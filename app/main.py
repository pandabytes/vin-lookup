import os
import fastparquet
import logging
from .apis.vpic import getVin, VpicApiError
from .apis.carImagery import getVehiclePhotoUrl, CarImageryApiError
from .config import Settings
from .db import entities, queries
from .dependencies.singletons import getSettings, getDbConnection, getLogger
from .schemas.lookup import LookupResponse
from .schemas.remove import RemoveResponse
from .utils.vin import isVinInCorrectFormat
from .utils.conversions import convertToDataFrame
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.responses import FileResponse
from pydantic import ValidationError
from sqlite3 import Connection

app = FastAPI()

def __validateVinFormat(vin: str):
  vin = vin.strip().upper()
  if not isVinInCorrectFormat(vin):
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"VIN {vin} must be a 17 alphanumeric characters string.")
  return vin

def __getVinViaVpic(vin: str, logger: logging.Logger):
  try:
    return getVin(vin)
  except VpicApiError as ex:
    logger.exception("Call to Vehicle API failed when looking up VIN %s. Error status code from Vehicle API is %d.", vin, ex.errorStatusCode)
    raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=f"Call to Vehicle API returned an error. Error: {ex}") from ex

def __getVehiclePhotoUrl(make: str, model: str, modelYear: str, logger: logging.Logger):
  try:
    return getVehiclePhotoUrl(make, model, modelYear)
  except CarImageryApiError as ex:
    loggedData = { "make": make, "model": model, "modelYear": modelYear }
    logger.exception("Call to CarImagery API failed when looking up vehicle photo using %s. Error status code from CarImagery API is %d.", loggedData, ex.errorStatusCode)
    raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=f"Call to CarImagery API returned an error. Error: {ex}") from ex

def __createEntityVin(vin: str, logger: logging.Logger):
  vpicVin = __getVinViaVpic(vin, logger)
  if vpicVin.make.strip() == "" or \
     vpicVin.model.strip() == "" or \
     vpicVin.modelYear.strip() == "" or \
     vpicVin.bodyClass.strip() == "":
    # This also means the data we get back from vpic API do not match with what we expect
    # We raise exception so that we don't need to send a request to Car Imagery to get the photo url
    # if the requested vin is not in the format we expect
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Cannot find VIN {vin}.")

  try:
    photoUrl = __getVehiclePhotoUrl(vpicVin.make, vpicVin.model, vpicVin.modelYear, logger)
    return entities.Vin(**vpicVin.dict(), photoUrl=photoUrl)
  except ValidationError as ex:
    # This also means the data we get back from vpic API do not match with what we expect
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Cannot find VIN {vin}.") from ex

@app.on_event("startup")
def startup():
  settings, logger = getSettings(), getLogger()
  logger.info(f"Connecting to vin cache at \"{settings.vinCacheFilePath}\".")
  _ = getDbConnection()

@app.on_event("shutdown")
def shutdown():
  logger = getLogger()
  logger.info("Shutting down service.")
  logger.info("Closing database connection.")
  dbConnection = getDbConnection()
  dbConnection.close()

@app.get("/lookup/{vin}", status_code=status.HTTP_200_OK)
def lookup(vin: str,
           logger: logging.Logger = Depends(getLogger),
           dbConnection: Connection = Depends(getDbConnection)):
  """ Lookup the given vin number in the cache. If the vin is not in the
      cache, then try to get it from [Vehicle API](https://vpic.nhtsa.dot.gov/api/)
      and insert the vin in the cache if found.
  """
  vin = __validateVinFormat(vin)
  
  # Try to get vin from cache first
  cacheVin = queries.getVin(dbConnection, vin)
  if cacheVin is not None:
    logger.info("Got VIN %s from cache.", vin)
    return LookupResponse(**cacheVin.dict(), cachedResult=True)
  
  entityVin = __createEntityVin(vin, logger)

  # Store vin in cache
  try:
    logger.info("Inserting VIN %s to cache.", vin)
    queries.insertVin(dbConnection, entityVin)
    return LookupResponse(**entityVin.dict(), cachedResult=False)
  except Exception as ex:
    logger.exception("Encountered unexpected error in trying to lookup VIN %s.", vin)
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Something happened on our end.") from ex

@app.delete("/remove/{vin}", status_code=status.HTTP_200_OK)
def remove(vin: str,
           logger: logging.Logger = Depends(getLogger),
           dbConnection: Connection = Depends(getDbConnection)):
  """ Remove the vin from cache. This API will return a status of 200, whether
      the vin was successfully removed or not from the cache. Client can use the 
      field `cacheDeleteSuccess` to check the actual success status of the API.
  """
  vin = __validateVinFormat(vin)
  try:
    isVinRemoved = queries.removeVin(dbConnection, vin)
    return RemoveResponse(vin=vin, cacheDeleteSuccess=isVinRemoved)
  except Exception as ex:
    logger.exception("Encountered unexpected error in trying to remove VIN %s. Error: %s", vin, ex)
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Something happened on our end.") from ex

@app.get("/export", status_code=status.HTTP_200_OK)
def export(logger: logging.Logger = Depends(getLogger),
           dbConnection: Connection = Depends(getDbConnection),
           settings: Settings = Depends(getSettings)):
  """ Export the cache to a parq file (Parquet format). If the cache is empty,
      then export an empty parq file.
  """
  # Always create an empty parquet file
  parquetFilePath = settings.parquetFilePath
  with open(parquetFilePath, "w") as _: 
    pass

  try:
    vins = queries.getAllVins(dbConnection)
    if len(vins) > 0:
      logger.info(f"Writing {len(vins)} vin(s) to file \"{parquetFilePath}\".")
      dataFrame = convertToDataFrame(vins)
      fastparquet.write(parquetFilePath, dataFrame)
  except Exception as ex:
    logger.exception("Encountered unexpected error in trying to export parq file. Error: %s", ex)
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Something happened on our end.") from ex

  return FileResponse(parquetFilePath, filename=os.path.basename(parquetFilePath))
