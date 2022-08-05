import pandas as pd
from ..db.entities import Vin

DATAFRAME_COLUMNS = ["vin", "make", "model", "modelYear", "bodyClass", "photoUrl"]

def convertToDataFrame(vins: list[Vin]):
  data = []
  for vin in vins:
    dataFrameRow = {
      DATAFRAME_COLUMNS[0]: vin.vin,
      DATAFRAME_COLUMNS[1]: vin.make,
      DATAFRAME_COLUMNS[2]: vin.model,
      DATAFRAME_COLUMNS[3]: vin.modelYear,
      DATAFRAME_COLUMNS[4]: vin.bodyClass,
      DATAFRAME_COLUMNS[5]: vin.photoUrl
    }
    data.append(dataFrameRow)

  return pd.DataFrame(data)



