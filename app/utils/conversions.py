import pandas as pd
from ..db.entities import Vin

def convertToDataFrame(vins: list[Vin]):
  data = []
  for vin in vins:
    dataFrameRow = {
      "vin": vin.vin,
      "make": vin.make,
      "model": vin.model,
      "modelYear": vin.modelYear,
      "bodyClass": vin.bodyClass
    }
    data.append(dataFrameRow)

  return pd.DataFrame(data)



