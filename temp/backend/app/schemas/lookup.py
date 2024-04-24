from pydantic import BaseModel

class LookupResponse(BaseModel):
  """ The response data returned by the `lookup` API. """
  vin: str
  make: str
  model: str
  modelYear: str
  bodyClass: str
  photoUrl = ""
  cachedResult: bool
