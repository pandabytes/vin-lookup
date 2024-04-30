from unittest.mock import MagicMock, patch, PropertyMock

import pytest
import requests

from ...apis.car_imagery import find_car_photo_url, CarImageryApiError

@pytest.mark.parametrize('make,model,model_year', [('', '', ''), ('', '  ', ' ')])
def test_find_car_photo_url_bad_arguments(make: str, model: str, model_year: str):
  with pytest.raises(ValueError):
    find_car_photo_url(make, model, model_year)

@pytest.mark.parametrize('error_status_code', [500, 400])
def test_find_car_photo_url_failed(error_status_code: int):
  with patch('requests.get') as mock_requests_get:
    dummy_response = requests.Response()
    dummy_response.status_code = error_status_code
    dummy_response.raise_for_status = MagicMock(side_effect=requests.HTTPError('Dummy HTTP error.'))
    mock_requests_get.return_value = dummy_response

    with pytest.raises(CarImageryApiError) as ex:
      find_car_photo_url('Toyota', 'Camry', '2020')
    assert ex.value.error_status_code == error_status_code

@pytest.mark.parametrize('xml_str', ['', '<xml></xml>', '<xml>', '<foo></bar>'])
def test_find_car_photo_url_returns_none(xml_str: str):
  with patch('requests.get') as mock_requests_get:
    with patch('requests.Response.text', new_callable=PropertyMock) as mock_response_text:
      mock_response_text.return_value = xml_str

      dummy_response = requests.Response()
      dummy_response.status_code = 200
      mock_requests_get.return_value = dummy_response   

      photo_url = find_car_photo_url('Toyota', 'Camry', '2020')
      assert photo_url is None

def test_find_car_photo_url_returns_photo_url():
  photo_url = find_car_photo_url('Toyota', 'Camry', '2020')
  assert photo_url != ''
