from urllib.parse import urlparse
from pydantic import BaseModel, ValidationInfo, field_validator

class Vin(BaseModel):
  """ The domain model that represents a VIN. """
  vin: str
  make: str
  model: str
  model_year: str
  body_class: str
  photo_url: str = ""

  class Config:
    from_attributes = True

  @field_validator('*')
  @classmethod
  def remove_whitespaces(cls, value: str) -> str:
    return value.strip()

  @field_validator('vin')
  @classmethod
  def make_vin_upper_case(cls, value: str) -> str:
    return value.upper()

  @field_validator('photo_url')
  @classmethod
  def is_photo_url_valid(cls, value: str) -> str:
    # Only check if photoUrl is provided
    if len(value) > 0 and not cls.is_url(value):
      raise ValueError(f"photoUrl is not a valid url \"{value}\".")
    return value

  @field_validator('vin')
  @classmethod
  def check_vin_format(cls, value: str) -> str:
    if not cls.is_vin_correct_format(value):
      raise ValueError(f"VIN \"{value}\" must be a 17 alphanumeric characters string.")
    return value

  @field_validator("vin", "make", "model", "model_year", "body_class")
  @classmethod
  def check_field_empty(cls, value: str, info: ValidationInfo) -> str:
    if len(value) == 0:
      raise ValueError(f"Field \"{info.field_name}\" must not be an empty string.")
    return value

  @classmethod
  def is_vin_correct_format(cls, vin: str) -> bool:
    """ Check if the given vin is 17 characters and
        all characters are alphanumeric.
    """
    return len(vin) == 17 and vin.isalnum()

  @classmethod
  def is_url(cls, url: str) -> bool:
    """ Taken from
        https://stackoverflow.com/questions/7160737/how-to-validate-a-url-in-python-malformed-or-not
    """
    try:
      result = urlparse(url)
      return all([result.scheme, result.netloc])
    except ValueError:
      return False
