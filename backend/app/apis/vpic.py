import requests
from pydantic import ValidationError
from .exceptions import ApiError
from ..schemas.vin import Vin

class VpicApiError(ApiError):
  pass

def find_vin(vin: str) -> Vin | None:
  if not Vin.is_vin_correct_format(vin):
    raise ValueError(f'VIN {vin} must be a 17 alphanumeric characters string.')

  response = requests.get(
    f'https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVinValues/{vin}?format=json',
    timeout=3
  )

  try:
    response.raise_for_status()
  except requests.HTTPError as ex:
    raise VpicApiError(f'Failed to get VIN {vin} from vpic API.', response.status_code) from ex

  json_obj = response.json()['Results'][0]
  try:
    return Vin(vin=vin,
               make=json_obj['Make'],
               model=json_obj['Model'],
               model_year=json_obj['ModelYear'],
               body_class=json_obj['BodyClass'])
  except ValidationError:
    return None
