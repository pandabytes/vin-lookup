import requests
import xml.etree.ElementTree as ET
from .exceptions import ApiError
from ..utils.url import isUrl

class CarImageryApiError(ApiError):
  pass

def getVehiclePhotoUrl(make: str, model: str, modelYear: str):
  # Make sure arguments aren't empty or whitespaces
  make, model, modelYear = make.strip(), model.strip(), modelYear.strip()
  if make == "" or model == "" or modelYear == "":
    raise ValueError("All arguments must not be empty string and not contain only whitespaces.")

  searchTerm = f"{make} {model} {modelYear}"
  response = requests.get(f"https://www.carimagery.com/api.asmx/GetImageUrl?searchTerm={searchTerm}")
  try:
    response.raise_for_status()
    root = ET.fromstring(response.text)
    url = root.text
    return url if isUrl(url) else None
  except requests.HTTPError as ex:
    raise CarImageryApiError(f"Failed to get photo url from CarImagery API.", response.status_code) from ex
