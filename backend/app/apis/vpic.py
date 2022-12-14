import requests
from .exceptions import ApiError
from ..utils.vin import isVinInCorrectFormat
from pydantic import BaseModel

class VpicApiError(ApiError):
  pass

class VpicVin(BaseModel):
  """ This simply a plain old data object. It only stores data, so no logic or validation. """
  vin: str
  make: str
  model: str
  modelYear: str
  bodyClass: str

def getVin(vin: str):
  if not isVinInCorrectFormat(vin):
    raise ValueError(f"VIN {vin} must be a 17 alphanumeric characters string.")

  response = requests.get(f"https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVinValues/{vin}?format=json")
  try:    
    response.raise_for_status()
  except requests.HTTPError as ex:
    raise VpicApiError(f"Failed to get VIN {vin} from vpic API.", response.status_code) from ex

  jsonObj = response.json()["Results"][0]
  return VpicVin(vin=vin,
                 make=jsonObj["Make"],
                 model=jsonObj["Model"],
                 modelYear=jsonObj["ModelYear"],
                 bodyClass=jsonObj["BodyClass"])
