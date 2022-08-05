import requests
import xml.etree.ElementTree as ET
from .exceptions import ApiError
from ..utils.url import isUrl

class CarImageryApiError(ApiError):
  pass

def getVehiclePhotoUrl(make: str, model: str, modelYear = ""):
  searchTerm = f"{make} {model} {modelYear}"
  response = requests.get(f"https://www.carimagery.com/api.asmx/GetImageUrl?searchTerm={searchTerm}")
  try:
    response.raise_for_status()
    root = ET.fromstring(response.text)
    url = root.text
    return url if isUrl(url) else None
  except requests.HTTPError as ex:
    raise CarImageryApiError(f"Failed to get photo url from CarImagery API.", response.status_code) from ex
