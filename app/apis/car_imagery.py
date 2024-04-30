from xml.etree import ElementTree

import requests

from .exceptions import ApiError
from ..schemas.vin import Vin

class CarImageryApiError(ApiError):
  pass

def find_car_photo_url(make: str, model: str, model_year: str) -> str | None:
  """ https://www.carimagery.com/api.pdf """
  # Make sure arguments aren't empty or whitespaces
  make, model, model_year = make.strip(), model.strip(), model_year.strip()
  if make == '' or model == '' or model_year == '':
    raise ValueError('All arguments must not be empty string and not contain only whitespaces.')

  search_term = f'{make} {model} {model_year}'
  response = requests.get(
    f'https://www.carimagery.com/api.asmx/GetImageUrl?searchTerm={search_term}',
    timeout=3
  )

  try:
    response.raise_for_status()
    root = ElementTree.fromstring(response.text)
    url = root.text
    return url if Vin.is_url(url) else None
  except ElementTree.ParseError:
    return None
  except requests.HTTPError as ex:
    raise CarImageryApiError(
      'Failed to get photo url from CarImagery API.',
      response.status_code
    ) from ex
