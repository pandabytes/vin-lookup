import os

def createSubdirs(path: str, isFilePath: bool):
  try:
    if isFilePath:
      # If path is a file path, then we remove the file name from the path
      # pathWithoutFileName = os.path.dirname(path)
      pathWithoutFileName, _ = os.path.split(path)
      if pathWithoutFileName != "":
        os.makedirs(pathWithoutFileName)
    else:
      os.makedirs(path)
  except FileExistsError:
    pass
