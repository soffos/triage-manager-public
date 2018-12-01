import inspect

def ensure_dict(func):
  def ensure(*args, **kwargs):
    try:
      data = args[inspect.getargspec(func)[0].index('data')]
    except NameError:
      print("No `data` variable passed")
      raise
    if not isinstance(data, dict):
      raise TypeError("`data` variable is not a dict")
    else:
      return func(*args, **kwargs)
  return ensure
