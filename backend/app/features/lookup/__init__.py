from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm.session import Session

from ...apis import vpic
from ...db.connection import get_db_session
from ...db.entities.vin import queries as vin_queries
from ...schemas.vin import Vin

router = APIRouter()

class LookupResponse(BaseModel):
  """ The response data returned by the `lookup` API. """
  vin: str
  make: str
  model: str
  model_year: str
  body_class: str
  photo_url: str = ''
  cached: bool = False

@router.get('/lookup/{vin}', status_code=status.HTTP_200_OK)
def lookup(vin: str, db_session: Session = Depends(get_db_session)):
  if not Vin.is_vin_correct_format(vin):
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                        detail='VIN must be a 17 alphanumeric characters string.')

  cache_vin = vin_queries.find_vin(db_session, vin)
  if cache_vin:
    return LookupResponse(**cache_vin.model_dump(), cached=True)

  try:
    fetched_vin = vpic.find_vin(vin)
    if fetched_vin:
      vin_queries.insert_vin(db_session, fetched_vin)
      return LookupResponse(**fetched_vin.model_dump(), cached=False)
  except vpic.VpicApiError as ex:
    raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                        detail=f'vpic API returns an error: {ex}.') from ex

  # VIN not found
  raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                      detail=f'VIN {vin} not found.')
