import pytest
import requests
from app.apis.vpic import getVin, VpicApiError
from unittest.mock import MagicMock, patch
from ..data import REAL_VINS, FAKE_VALID_FORMAT_VIN

@pytest.mark.parametrize("vin", ["xxxxxxxxxxxxxxxxxx", "xxxxxxxxxxxxxxxx;", "123"])
def test_getVin_bad_format_vin(vin: str):
  with pytest.raises(ValueError):
    getVin(vin)

@pytest.mark.parametrize("errorStatusCode", [500, 400])
def test_getVin_vpic_api_failed(errorStatusCode: int):
  with patch("requests.get") as mockRequestsGet:
    dummyResponse = requests.Response()
    dummyResponse.status_code = errorStatusCode
    dummyResponse.raise_for_status = MagicMock(side_effect=requests.HTTPError("Dummy HTTP error"))
    mockRequestsGet.return_value = dummyResponse

    with pytest.raises(VpicApiError) as ex:
      getVin(FAKE_VALID_FORMAT_VIN)
    assert ex.value.errorStatusCode == errorStatusCode

def test_getVin_returns_vin_object():
  vpicVin = getVin(REAL_VINS[0])
  assert vpicVin.vin != ""
  assert vpicVin.make != ""
  assert vpicVin.model != ""
  assert vpicVin.modelYear != ""
  assert vpicVin.bodyClass != ""
