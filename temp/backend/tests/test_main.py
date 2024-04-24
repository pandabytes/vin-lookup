import app.main as main
import fastparquet
import os
import pytest
from app.schemas.remove import RemoveResponse
from app.schemas.lookup import LookupResponse
from app.utils.conversions import DATAFRAME_COLUMNS
from fastapi.testclient import TestClient
from fastapi import status
from .data import REAL_VINS, FAKE_VALID_FORMAT_VIN

client = TestClient(main.app)

def removeInsertedVins(vins: list[str]):
  """ The vin cache persists until the application is shutdown, so we
      have to remove the inserted vin just in case subsequent tests
      also use the same vin number.
  """
  for vin in vins:
    response = client.delete(f"/remove/{vin}")
    assert response.status_code == status.HTTP_200_OK

def insertVins(vins: list[str]) -> list[LookupResponse]:
  """ Add multiple vins to the cache. """
  lookupResponses = []
  for vin in vins:
    response = client.get(f"/lookup/{vin}")
    assert response.status_code == status.HTTP_200_OK
    lookupResponses.append(LookupResponse(**response.json()))
  return lookupResponses

class TestLookupApi:
  @pytest.mark.parametrize("vin", ["xxxxxxxxxxxxxxxxxx", "xxxxxxxxxxxxxxxx;", "123"])
  def test_lookup_bad_format_vin(self, vin: str):
    response = client.get(f"/lookup/{vin}")
    assert response.status_code == status.HTTP_400_BAD_REQUEST

  def test_lookup_vin_not_found(self):
    response = client.get(f"/lookup/{FAKE_VALID_FORMAT_VIN}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    
  @pytest.mark.parametrize("vin", REAL_VINS)
  def test_lookup_vin_found_but_not_in_cache(self, vin: str):
    response = client.get(f"/lookup/{vin}")
    assert response.status_code == status.HTTP_200_OK

    lookupResponse = LookupResponse(**response.json())
    assert lookupResponse.cachedResult == False

    removeInsertedVins([vin])

  def test_lookup_vin_found_in_cache(self):
    vin = REAL_VINS[0]
    response = client.get(f"/lookup/{vin}")
    assert response.status_code == status.HTTP_200_OK

    lookupResponse = LookupResponse(**response.json())
    assert lookupResponse.cachedResult == False

    # This time the vin should be in the cache
    response = client.get(f"/lookup/{vin}")
    assert response.status_code == status.HTTP_200_OK

    lookupResponse = LookupResponse(**response.json())
    assert lookupResponse.cachedResult == True

    removeInsertedVins([vin])

class TestRemoveApi:
  @pytest.mark.parametrize("vin", ["xxxxxxxxxxxxxxxxxx", "xxxxxxxxxxxxxxxx;", "123"])
  def test_remove_bad_format_vin(self, vin: str):
    response = client.delete(f"/remove/{vin}")
    assert response.status_code == status.HTTP_400_BAD_REQUEST

  def test_remove_vin_not_in_cache(self):
    response = client.delete(f"/remove/{FAKE_VALID_FORMAT_VIN}")
    assert response.status_code == status.HTTP_200_OK

    removeResponse = RemoveResponse(**response.json())
    assert removeResponse.cacheDeleteSuccess == False

  def test_remove_vin_in_cache(self):
    vin = REAL_VINS[0]

    response = client.get(f"/lookup/{vin}")
    assert response.status_code == status.HTTP_200_OK

    response = client.delete(f"/remove/{vin}")
    assert response.status_code == status.HTTP_200_OK

    removeResponse = RemoveResponse(**response.json())
    assert removeResponse.cacheDeleteSuccess == True

class TestExportApi:
  def test_export_with_vins_in_cache(self):
    # Add some vins to the cache so that we can export non-empty cache
    vins = REAL_VINS
    expectedVins = insertVins(vins)

    # Export the cache
    response = client.get("/export")
    assert response.status_code == status.HTTP_200_OK

    # Write the exported content to a temporary file
    downloadFilePath = "download_vin_cache.parq"
    with open(downloadFilePath, "wb") as cacheFile:
      cacheFile.write(response.content)
    
    try:
      # Read the download file to Dataframe so that we can assert
      # the exported content against the content we inserted earlier
      parqFile = fastparquet.ParquetFile(downloadFilePath)
      cacheDf = parqFile.to_pandas()

      # Assert dimensions of cacheDf
      assert cacheDf.shape[0] == len(vins)
      assert cacheDf.shape[1] == len(DATAFRAME_COLUMNS)

      for (expectedVin , (_, actualVin)) in zip(expectedVins, cacheDf.iterrows()):
        assert expectedVin.vin == actualVin.vin
        assert expectedVin.make == actualVin.make
        assert expectedVin.model == actualVin.model
        assert expectedVin.modelYear == actualVin.modelYear
        assert expectedVin.bodyClass == actualVin.bodyClass
        assert expectedVin.photoUrl == actualVin.photoUrl  
    finally:
      removeInsertedVins(vins)
      os.remove(downloadFilePath)
    
  def test_export_with_no_vin_in_cache(self):
    # Export the cache
    response = client.get(f"/export")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.content) == 0
