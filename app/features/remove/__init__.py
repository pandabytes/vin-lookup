from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm.session import Session

from ...db.connection import get_db_session
from ...db.entities.vin import queries as vin_queries
from ...schemas.vin import Vin

router = APIRouter()

class RemoveResponse(BaseModel):
  """ The response data returned by the `remove` API. """
  vin: str
  cache_delete_success: bool

@router.delete("/remove/{vin}", status_code=status.HTTP_200_OK)
def remove(vin: str, db_session: Session = Depends(get_db_session)) -> RemoveResponse:
  if not Vin.is_vin_correct_format(vin):
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                        detail='VIN must be a 17 alphanumeric characters string.')

  vin_removed = vin_queries.remove_vin(db_session, vin)
  return RemoveResponse(vin=vin, cache_delete_success=vin_removed)
