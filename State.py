class State:
  x = 0
  y = 0

  def __init__(self, x, y):
    self.x = x
    self.y = y
    
  def __eq__(self, other):
    if self.x==other.x and self.y==other.y:
      return True
    else:
      return False
  
  def __hash__(self):
    return hash(tuple((self.x, self.y)))