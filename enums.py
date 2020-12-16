from enum import Enum

class Action(Enum):
  UP = 0
  Down = 1
  Right = 2
  Left = 3

'''block value convension
      0: Open block
      1: Got to Power Position
      2: Restart
      3: Wall
      4: Goal
      5: Power position
      6: Start
'''
class CellState(Enum):
  Open = 0
  GOTOPower = 1
  Restart = 2
  Wall = 3
  Goal = 4
  Power = 5
  Start = 6