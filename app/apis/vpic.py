import requests
from .exceptions import ApiError
from ..db.entities import Vin
from ..utils.vin import isVinInCorrectFormat
from pydantic import ValidationError

class VpicApiError(ApiError):
  pass

def getVin(vin: str):
  if not isVinInCorrectFormat(vin):
    raise ValueError(f"VIN {vin} must be a 17 alphanumeric characters string.")

  response = requests.get(f"https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVinValues/{vin}?format=json")
  try:    
    response.raise_for_status()
  except requests.HTTPError as ex:
    raise VpicApiError(f"Failed to get VIN {vin} from vpic API.", response.status_code) from ex
    
  try:
    jsonObj = response.json()["Results"][0]

    return Vin(vin=vin, 
               make=jsonObj["Make"],
               model=jsonObj["Model"],
               modelYear=jsonObj["ModelYear"],
               bodyClass=jsonObj["BodyClass"])
  except ValidationError:    
    return None