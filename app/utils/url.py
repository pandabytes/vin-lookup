from urllib.parse import urlparse

def isUrl(url):
  """ Taken from https://stackoverflow.com/questions/7160737/how-to-validate-a-url-in-python-malformed-or-not """
  try:
    result = urlparse(url)
    return all([result.scheme, result.netloc])
  except ValueError:
    return False
