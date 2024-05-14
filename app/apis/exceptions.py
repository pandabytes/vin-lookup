from pydantic.dataclasses import dataclass

@dataclass
class ApiError(Exception):
  message: str
  error_status_code: int
