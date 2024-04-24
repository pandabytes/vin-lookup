from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm.session import Session

from backend.app.db.connection import get_db_session
from backend.app.db.entities.vin import queries as vin_queries
from backend.app.schemas.vin import Vin

router = APIRouter()

class LookupResponse(BaseModel):
  """ The response data returned by the `lookup` API. """
  vin: str
  make: str
  model: str
  model_year: str
  body_class: str
  photo_url: str = ""

@router.get('/lookup/{vin}', status_code=status.HTTP_200_OK)
def lookup(vin: str, db_session: Session = Depends(get_db_session)):
  if not Vin.is_vin_correct_format(vin):
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                        detail='VIN must be a 17 alphanumeric characters string.')

  cache_vin = vin_queries.find_vin(db_session, vin)
  if not cache_vin:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f'VIN {vin} not found.')

  return LookupResponse(**cache_vin.model_dump())
