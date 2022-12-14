from pydantic import BaseModel, BaseSettings, Field, fields, validator
from typing import Any

class Settings(BaseSettings):
  vinCacheFilePath: str = Field(default="./.temp/vinCache.db", env='VIN_CACHE_FILE_PATH')
  parquetFilePath: str = Field(default="./.temp/vins.parq", env='PARQUET_FILE_PATH')

  @validator("*", pre=True)
  def removeWhitespaces(cls, value: str):
    return value.strip()

  @validator("*")
  def checkFieldIsEmpty(cls, value: str, field: fields.ModelField):
    if len(value.strip()) == 0:
      raise ValueError(f"Field \"{field}\" must not be an empty string.")
    return value

class LogConfig(BaseModel):
    """ Logging configuration """
    logFormat: str = "%(levelprefix)s %(asctime)s - %(message)s"
    version = 1
    disable_existing_loggers = False
    formatters = {
      "default": {
          "()": "uvicorn.logging.DefaultFormatter",
          "fmt": logFormat,
          "datefmt": "%Y/%m/%d %H:%M:%S",
      },
    }
    handlers = {
      "default": {
          "formatter": "default",
          "class": "logging.StreamHandler",
          "stream": "ext://sys.stdout",
      },
    }
    loggers: dict[str, dict[str, Any]] = {}

    def addLogger(self, loggerName: str, logLevel: int | str):
      """ Add a logger to the configuration. Once a logger is added to the 
          configuration, we can get the logger via the `logging` library.

          Example:
          ```py
          import logging
          from logging.config import dictConfig
          
          loggerName, logConfig = "foo", LogConfig()
          logConfig.addLogger(loggerName, "INFO")

          dictConfig(logConfig.dict())
          logger = logging.getLogger(loggerName)
          ```
      """
      self.loggers[loggerName] = { "handlers": ["default"], "level": logLevel }
