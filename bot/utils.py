import validators

def is_valid_url(url: str) -> bool:
  try:
    validators.url(url)
    return True
  except validators.ValidationError:
    return False