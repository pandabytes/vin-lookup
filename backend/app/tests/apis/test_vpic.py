from unittest.mock import MagicMock, patch
import pytest
import requests

from ...apis.vpic import find_vin, VpicApiError
from ..data import REAL_VINS, FAKE_VALID_FORMAT_VIN

@pytest.mark.parametrize("vin", ["xxxxxxxxxxxxxxxxxx", "xxxxxxxxxxxxxxxx;", "123"])
def test_find_vin_bad_format_vin(vin: str):
  with pytest.raises(ValueError):
    find_vin(vin)

@pytest.mark.parametrize("error_status_code", [500, 400])
def test_find_vin_vpic_api_failed(error_status_code: int):
  with patch("requests.get") as mock_requests_get:
    dummy_response = requests.Response()
    dummy_response.status_code = error_status_code
    dummy_response.raise_for_status = MagicMock(side_effect=requests.HTTPError("Dummy HTTP error"))
    mock_requests_get.return_value = dummy_response

    with pytest.raises(VpicApiError) as ex:
      find_vin(FAKE_VALID_FORMAT_VIN)
    assert ex.value.error_status_code == error_status_code

def test_find_vin_returns_vin_object():
  vin = find_vin(REAL_VINS[0])
  assert vin.vin != ""
  assert vin.make != ""
  assert vin.model != ""
  assert vin.model_year != ""
  assert vin.body_class != ""
