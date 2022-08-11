import pytest
import requests
from app.apis.carImagery import getVehiclePhotoUrl, CarImageryApiError
from unittest.mock import MagicMock, patch, PropertyMock

@pytest.mark.parametrize("make,model,modelYear", [("", "", ""), ("", "  ", " ")])
def test_getVehiclePhotoUrl_bad_arguments(make: str, model: str, modelYear: str):
  with pytest.raises(ValueError):
    getVehiclePhotoUrl(make, model, modelYear)

@pytest.mark.parametrize("errorStatusCode", [500, 400])
def test_getVehiclePhotoUrl_carImagery_api_failed(errorStatusCode: int):
  with patch("requests.get") as mockRequestsGet:
    dummyResponse = requests.Response()
    dummyResponse.status_code = errorStatusCode
    dummyResponse.raise_for_status = MagicMock(side_effect=requests.HTTPError("Dummy HTTP error."))
    mockRequestsGet.return_value = dummyResponse

    with pytest.raises(CarImageryApiError) as ex:
      getVehiclePhotoUrl("Toyota", "Camry", "2020")
    assert ex.value.errorStatusCode == errorStatusCode

def test_getVehiclePhotoUrl_returns_None():
  with patch("requests.get") as mockRequestsGet:
    with patch("requests.Response.text", new_callable=PropertyMock) as mockResponseText:
      mockResponseText.return_value = "<xml></xml>"
      
      dummyResponse = requests.Response()
      dummyResponse.status_code = 200
      mockRequestsGet.return_value = dummyResponse   

      photoUrl = getVehiclePhotoUrl("Toyota", "Camry", "2020")
      assert photoUrl is None

def test_getVehiclePhotoUrl_returns_photo_url():
  photoUrl = getVehiclePhotoUrl("Toyota", "Camry", "2020")
  assert photoUrl != ""
