import sqlite3
from contextlib import closing
from pydantic.dataclasses import dataclass
from .entities import Vin

@dataclass
class DatabaseError(Exception):
  message: str

def connectToVinDatabase(filePath: str):
  """ Connect to the Vin database cache. This returns a connection object
      in which must be manually closed by the client.
  """
  try:
    connection = sqlite3.connect(filePath, check_same_thread=False)
    with closing(connection.cursor()) as cursor:
      # This ensures we always have fresh table 
      cursor.execute("DROP TABLE IF EXISTS Vin")

      cursor.execute("""
        CREATE TABLE IF NOT EXISTS Vin (
          vin TEXT PRIMARY KEY,
          make TEXT NOT NULL,
          model TEXT NOT NULL,
          modelYear TEXT NOT NULL,
          bodyClass TEXT NOT NULL,
          photoUrl TEXT NOT NULL
        )
      """)

      connection.commit()
      return connection
  except Exception as ex:
    raise DatabaseError(f"Failed to connect to sqlite at \"{filePath}\".") from ex

def insertVin(connection: sqlite3.Connection, vin: Vin):
  """ Insert `vin` to the the Vin table. """
  try:
    with closing(connection.cursor()) as cursor:
      insertParams = (vin.vin, vin.make, vin.model, vin.modelYear, vin.bodyClass, vin.photoUrl)
      cursor.execute("INSERT INTO Vin VALUES (?, ?, ?, ?, ?, ?)", insertParams)
      connection.commit()
  except Exception as ex:
    raise DatabaseError(f"Failed to insert \"{vin}\".") from ex
  
def getVin(connection: sqlite3.Connection, vin: str) -> Vin | None:
  """ Get the `vin` from the Vin table. If not found, None is returned. """
  try:
    with closing(connection.cursor()) as cursor:
      rows = cursor.execute("SELECT * FROM Vin WHERE vin = :vin", { "vin": vin })
      firstRow = rows.fetchone()
      if firstRow is None:
        return None
      return __mapRowToVin(firstRow)
  except Exception as ex:
    raise DatabaseError(f"Failed to get vin {vin}.") from ex

def getAllVins(connection: sqlite3.Connection) -> list[Vin]:
  """ Get all vins in the cache. """
  try:
    with closing(connection.cursor()) as cursor:
      rows = cursor.execute("SELECT * FROM Vin")
      return [__mapRowToVin(row) for row in rows]
  except Exception as ex:
    raise DatabaseError(f"Failed to get all vins in database.") from ex

def removeVin(connection: sqlite3.Connection, vin: str):
  """ Remove the `vin` from the Vin table. It returns `True` if the vin was removed. `False` otherwise. """
  try:
    with closing(connection.cursor()) as cursor:
      rows = cursor.execute("DELETE FROM Vin WHERE vin = :vin", { "vin": vin })
      connection.commit()
      return rows.rowcount == 1
  except Exception as ex:
    raise DatabaseError(f"Failed to remove vin {vin}.") from ex

def __mapRowToVin(row: tuple) -> Vin:
  """ Attempt to map the raw data from sqlite (tuple) to Vin object. """
  try:
    return Vin(vin=row[0],
               make=row[1],
               model=row[2],
               modelYear=row[3],
               bodyClass=row[4],
               photoUrl=row[5])
  except Exception as ex:
    raise ValueError(f"Unable to map from object {row} to Vin entity object.") from ex
