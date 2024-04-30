from fastapi import APIRouter, Depends, status
from pydantic import BaseModel
from sqlalchemy.orm.session import Session

from ...db.connection import get_db_session
from ...db.entities.vin import queries as vin_queries
from ...schemas.vin import Vin

router = APIRouter()

class ListResponse(BaseModel):
  """ The response data returned by the `list` API. """
  vins: list[Vin]

@router.get('/list', status_code=status.HTTP_200_OK)
def list_vins(db_session: Session = Depends(get_db_session)) -> ListResponse:
  vins = vin_queries.get_all_vins(db_session)
  return ListResponse(vins=vins)
