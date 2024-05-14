from sqlalchemy import Column, Integer, String
from ...connection import Base

class VinEntity(Base):
  """ The entity that models the data in the Vin cache. """
  __tablename__ = 'vin'

  id = Column(Integer, primary_key=True)
  vin = Column(String(length=17), unique=True, index=True, nullable=False)
  make = Column(String, nullable=False)
  model = Column(String, nullable=False)
  model_year = Column(String, nullable=False)
  body_class = Column(String, nullable=False)
  photo_url = Column(String, nullable=False)
