
import logging
from ..config import Settings, LogConfig
from ..db import queries
from ..utils.file import createSubdirs
from functools import lru_cache
from logging.config import dictConfig

@lru_cache()
def getSettings():
  settings = Settings()
  
  # Create subdirectories for files
  createSubdirs(settings.vinCacheFilePath, True)
  createSubdirs(settings.parquetFilePath, True)

  return settings

@lru_cache()
def getDbConnection():
  settings = getSettings()
  return queries.connectToVinDatabase(settings.vinCacheFilePath)

@lru_cache
def getLogger():
  # Set up logging
  loggerName, logConfig = __name__, LogConfig()
  logConfig.addLogger(loggerName, "INFO")

  dictConfig(logConfig.dict())
  return logging.getLogger(loggerName)
