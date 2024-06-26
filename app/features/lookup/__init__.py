from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm.session import Session

from ...apis import car_imagery, vpic
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
def lookup(vin: str, db_session: Session = Depends(get_db_session)) -> LookupResponse:
  if not Vin.is_vin_correct_format(vin):
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                        detail='VIN must be a 17 alphanumeric characters string.')

  cache_vin = vin_queries.find_vin(db_session, vin)
  if cache_vin:
    return LookupResponse(**cache_vin.model_dump(), cached=True)

  try:
    fetched_vin = vpic.find_vin(vin)
    if not fetched_vin:
      # VIN not found
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                          detail=f'VIN {vin} not found.')

    # Attempt to find an image of this car
    photo_url = car_imagery.find_car_photo_url(
      fetched_vin.make, fetched_vin.model, fetched_vin.model_year
    ) or ''

    fetched_vin.photo_url = photo_url
    vin_queries.insert_vin(db_session, fetched_vin)
    return LookupResponse(**fetched_vin.model_dump(), cached=False)
  except vpic.VpicApiError as ex:
    raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                        detail=f'vpic API returns an error: {ex}.') from ex
  except car_imagery.CarImageryApiError as ex:
    raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                        detail=f'CarImagery API returns an error: {ex}.') from ex
