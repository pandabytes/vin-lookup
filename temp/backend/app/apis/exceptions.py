from pydantic.dataclasses import dataclass

@dataclass
class ApiError(Exception):
  message: str
  errorStatusCode: int
