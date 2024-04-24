from sqlalchemy.orm import Session
from backend.app.schemas import Vin
from .entity import VinEntity

def find_vin(db: Session, vin: str) -> VinEntity | None:
  """ x """
  return db.query(VinEntity).filter(VinEntity.vin == vin).first()

def insert_vin(db: Session, vin: Vin):
  vin_entity = VinEntity(
    vin=vin.vin,
    make=vin.make,
    model=vin.model,
    model_year=vin.model_year,
    body_class=vin.body_class,
    photo_url=vin.photo_url,
  )
  db.add(vin_entity)
  db.commit()
