import csv
import os
import fastparquet
import pandas as pd
import pytest
from fastapi.testclient import TestClient
from fastapi import status

from ..main import app
from .data import REAL_VINS, FAKE_VALID_FORMAT_VIN
from ..features.lookup import LookupResponse
from ..features.remove import RemoveResponse
from ..features.list_vins import ListResponse
from ..schemas import Vin

@pytest.fixture(autouse=True, scope='function')
def client():
  with TestClient(app) as test_client:
    yield test_client

    # The vin cache persists until the application is shutdown, so we
    # have to remove the inserted vin just in case subsequent tests
    # also use the same vin number.
    list_response = ListResponse(**test_client.get('/list').json())
    for vin in list_response.vins:
      response = test_client.delete(f'/remove/{vin.vin}')
      assert response.status_code == status.HTTP_200_OK

class TestLookupApi:
  @pytest.mark.parametrize('vin', ['xxxxxxxxxxxxxxxxxx', 'xxxxxxxxxxxxxxxx;', '123'])
  def test_lookup_bad_format_vin(self, vin: str, client: TestClient):
    response = client.get(f'/lookup/{vin}')
    assert response.status_code == status.HTTP_400_BAD_REQUEST

  def test_lookup_vin_not_found(self, client: TestClient):
    response = client.get(f'/lookup/{FAKE_VALID_FORMAT_VIN}')
    assert response.status_code == status.HTTP_404_NOT_FOUND

  @pytest.mark.parametrize('vin', REAL_VINS)
  def test_lookup_vin_found_but_not_in_cache(self, vin: str, client: TestClient):
    # Arrange
    response = client.get(f'/lookup/{vin}')
    assert response.status_code == status.HTTP_200_OK

    # Act
    response = LookupResponse(**response.json())

    # Assert
    assert not response.cached

  def test_lookup_vin_found_in_cache(self, client: TestClient):
    # Arrange
    vin = REAL_VINS[0]
    response = client.get(f'/lookup/{vin}')
    assert response.status_code == status.HTTP_200_OK

    lookup_response = LookupResponse(**response.json())
    assert not lookup_response.cached

    # Act
    # This time the vin should be in the cache
    response = client.get(f'/lookup/{vin}')
    assert response.status_code == status.HTTP_200_OK

    # Assert
    lookup_response = LookupResponse(**response.json())
    assert lookup_response.cached

class TestRemoveApi:
  @pytest.mark.parametrize('vin', ['xxxxxxxxxxxxxxxxxx', 'xxxxxxxxxxxxxxxx;', '123'])
  def test_remove_bad_format_vin(self, vin: str, client: TestClient):
    response = client.delete(f'/remove/{vin}')
    assert response.status_code == status.HTTP_400_BAD_REQUEST

  def test_remove_vin_not_in_cache(self, client: TestClient):
    # Act
    response = client.delete(f'/remove/{FAKE_VALID_FORMAT_VIN}')

    # Assert
    assert response.status_code == status.HTTP_200_OK

    remove_response = RemoveResponse(**response.json())
    assert not remove_response.cache_delete_success

  def test_remove_vin_in_cache(self, client: TestClient):
    # Arrange
    vin = REAL_VINS[0]

    response = client.get(f'/lookup/{vin}')
    assert response.status_code == status.HTTP_200_OK

    # Act
    response = client.delete(f'/remove/{vin}')

    # Assert
    assert response.status_code == status.HTTP_200_OK

    remove_response = RemoveResponse(**response.json())
    assert remove_response.cache_delete_success

class TestExportApi:
  @pytest.mark.parametrize('export_format', ['csv', 'parquet'])
  def test_export_with_vins_in_cache(self, client: TestClient, export_format: str):
    # Arrange
    # Add some vins to the cache so that we can export non-empty cache
    vins = REAL_VINS
    expected_vins = self._insert_vins(vins, client)

    # Act
    response = client.get(f'/export?export_format={export_format}')
    assert response.status_code == status.HTTP_200_OK

    # Assert
    # Write the exported content to a temporary file
    download_file_path = f'download_vin_cache.{export_format}'
    with open(download_file_path, 'wb') as cache_file:
      cache_file.write(response.content)

    try:
      # Read the download file to Dataframe so that we can assert
      # the exported content against the content we inserted earlier
      cache_df: pd.DataFrame
      if export_format == 'csv':
        cache_df = pd.read_csv(download_file_path, sep=',', header=0, dtype=str)
      elif export_format == 'parquet':
        parq_file = fastparquet.ParquetFile(download_file_path)
        cache_df = parq_file.to_pandas()
      else:
        raise ValueError(f'Export format {export_format} not supported in test.')

      # Assert dimensions of cache_df
      assert cache_df.shape[0] == len(vins)
      assert cache_df.shape[1] == 6

      for (expected_vin , (_, actual_vin)) in zip(expected_vins, cache_df.iterrows()):
        assert expected_vin.vin == actual_vin.vin
        assert expected_vin.make == actual_vin.make
        assert expected_vin.model == actual_vin.model
        assert expected_vin.model_year == actual_vin.model_year
        assert expected_vin.body_class == actual_vin.body_class
        assert expected_vin.photo_url == actual_vin.photo_url
    finally:
      os.remove(download_file_path)

  def test_export_with_no_vin_in_cache(self, client: TestClient):
    # Act
    response = client.get('/export')

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert response.json() is None

  @classmethod
  def _insert_vins(cls, vins: list[str], client: TestClient) -> list[Vin]:
    ''' Add multiple vins to the cache. '''
    inserted_vins = []
    for vin in vins:
      response = client.get(f'/lookup/{vin}')
      assert response.status_code == status.HTTP_200_OK
      inserted_vins.append(Vin(**response.json()))
      # lookup_responses.append(LookupResponse(**response.json()))
    return inserted_vins
