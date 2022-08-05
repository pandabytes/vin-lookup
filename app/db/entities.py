from pydantic import BaseModel, validator, fields
from ..utils.vin import isVinInCorrectFormat
from ..utils.url import isUrl

class Vin(BaseModel):
  """ The entity that models the data in the Vin cache. """
  vin: str
  make: str
  model: str
  modelYear: str
  bodyClass: str
  photoUrl = ""

  @validator("vin", pre=True)
  def makeVinUpperCase(cls, value: str):
    return value.upper()

  @validator("*", pre=True)
  def removeWhitespaces(cls, value: str):
    return value.strip()

  @validator("photoUrl")
  def isPhotoUrlValidUrl(cls, value: str):
    # Only check if photoUrl is provided
    if len(value) > 0 and not isUrl(value):
      raise ValueError(f"photoUrl is not a valid url \"{value}\".")
    return value

  @validator("vin")
  def checkVinInCorrectFormat(cls, value: str):
    if not isVinInCorrectFormat(value):
      raise ValueError(f"VIN \"{value}\" must be a 17 alphanumeric characters string.")
    return value

  @validator("vin", "make", "model", "modelYear", "bodyClass")
  def checkFieldIsEmpty(cls, value: str, field: fields.ModelField):
    if len(value) == 0:
      raise ValueError(f"Field \"{field}\" must not be an empty string.")
    return value
