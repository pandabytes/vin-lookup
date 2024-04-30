import tempfile

from enum import Enum

import fastparquet
import pandas as pd
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy.orm.session import Session

from ...db.connection import get_db_session
from ...db.entities.vin import queries as vin_queries
from ...schemas.vin import Vin

class ExportFormat(str, Enum):
  CSV = 'csv'
  PARQUET = 'parquet'

router = APIRouter()

@router.get('/export', status_code=status.HTTP_200_OK)
def export(
  background_tasks: BackgroundTasks,
  export_format: ExportFormat = ExportFormat.CSV,
  db_session: Session = Depends(get_db_session)
) -> FileResponse:
  vins = vin_queries.get_all_vins(db_session)
  if not vins:
    return None

  # Create a temp file to store the vins
  temp_file = tempfile.NamedTemporaryFile(delete_on_close=True)
  file_path = temp_file.name

  try:
    # After we return successfully, run background task to delete the temp file
    background_tasks.add_task(temp_file.close)

    df = _convert_to_dataframe(vins)

    match export_format:
      case ExportFormat.CSV:
        df.to_csv(file_path, header=True, sep=',', index=False)
      case ExportFormat.PARQUET:
        fastparquet.write(file_path, df)
      case _:
        raise NotImplementedError(f'Export format {export_format} is not supported.')

    return FileResponse(
      file_path,
      filename=f'vins_cache.{export_format.value}',
    )
  except:
    # Close the file when something unexpected happened
    temp_file.close()
    raise

def _convert_to_dataframe(vins: list[Vin]) -> pd.DataFrame:
  df_columns = ['vin', 'make', 'model', 'model_year', 'body_class', 'photo_url']
  data = []

  for vin in vins:
    df_row = {
      df_columns[0]: vin.vin,
      df_columns[1]: vin.make,
      df_columns[2]: vin.model,
      df_columns[3]: vin.model_year,
      df_columns[4]: vin.body_class,
      df_columns[5]: vin.photo_url
    }
    data.append(df_row)

  return pd.DataFrame(data)
