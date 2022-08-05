import sqlite3
from contextlib import closing
from .entities import Vin

def connectToVinDatabase(filePath: str):
  """ Connect to the Vin database cache. This returns a connection object
      in which must be manually closed by the client.
  """
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
    raise ValueError(f"Unable to map from object {row} to Vin entity object. Error: {ex}")

def insertVin(connection: sqlite3.Connection, vin: Vin):
  """ Insert `vin` to the the Vin table. """
  with closing(connection.cursor()) as cursor:
    insertParams = (vin.vin, vin.make, vin.model, vin.modelYear, vin.bodyClass, vin.photoUrl)
    cursor.execute("INSERT INTO Vin VALUES (?, ?, ?, ?, ?, ?)", insertParams)
    connection.commit()
  
def getVin(connection: sqlite3.Connection, vin: str) -> Vin | None:
  """ Get the `vin` from the Vin table. If not found, None is returned. """
  with closing(connection.cursor()) as cursor:
    rows = cursor.execute("SELECT * FROM Vin WHERE vin = :vin", { "vin": vin })
    firstRow = rows.fetchone()
    if firstRow is None:
      return None

    return __mapRowToVin(firstRow)

def getAllVins(connection: sqlite3.Connection) -> list[Vin]:
  """ Get all vins in the cache. """
  with closing(connection.cursor()) as cursor:
    rows = cursor.execute("SELECT * FROM Vin")
    return [__mapRowToVin(row) for row in rows]

def removeVin(connection: sqlite3.Connection, vin: str):
  """ Remove the `vin` from the Vin table. It returns `True` if the vin was removed. `False` otherwise. """
  with closing(connection.cursor()) as cursor:
    rows = cursor.execute("DELETE FROM Vin WHERE vin = :vin", { "vin": vin })
    connection.commit()
    return rows.rowcount == 1
