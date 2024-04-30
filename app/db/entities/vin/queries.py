from sqlalchemy.orm import Session
from ....schemas import Vin
from .entity import VinEntity

def get_all_vins(db: Session) -> list[Vin]:
  return [
    Vin(
      vin=vin_entity.vin,
      make=vin_entity.make,
      model=vin_entity.model,
      model_year=vin_entity.model_year,
      body_class=vin_entity.body_class,
      photo_url=vin_entity.photo_url,
    )
    for vin_entity in db.query(VinEntity).all()
  ]

def find_vin(db: Session, vin: str) -> Vin | None:
  vin_entity = db.query(VinEntity).filter(VinEntity.vin == vin).first()
  if not vin_entity:
    return None

  return Vin(
    vin=vin_entity.vin,
    make=vin_entity.make,
    model=vin_entity.model,
    model_year=vin_entity.model_year,
    body_class=vin_entity.body_class,
    photo_url=vin_entity.photo_url,
  )

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

def remove_vin(db: Session, vin: str) -> bool:
  removed_count = (db
    .query(VinEntity)
    .filter(VinEntity.vin == vin)
    .delete()
  )

  db.commit()
  return removed_count == 1
