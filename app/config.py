from pydantic import BaseSettings, Field

class Settings(BaseSettings):
  vinCacheFilePath: str = Field(default="./vinCache.db", env='VIN_CACHE_FILE_PATH')
