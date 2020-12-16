from random import randint
from enums import Action, CellState
from State import State
import math

class environment:
  _grid = [[]]
  _powerX, _powerY = 4,7
  _power = State(_powerX, _powerY)
  _startX, _startY = 0,0
  _start = State(_startX, _startY)
  #init varibale only, will update in generateGrid function
  _goal = State(_startX, _startY)
  _rows = _cols = 8
  
  def __init__(self):
    self._grid = self.generateGrid()

  def generateGrid(self):
    grid = [ [ CellState.Open for i in range(self._rows) ] for j in range(self._cols) ]

    #set "Got to Power Position" blocks
    grid[0][7] = grid[5][1] = grid[6][3] = CellState.GOTOPower

    #set "Restart" blocks
    grid[3][0] = grid[3][6] = CellState.Restart

    #set "Wall" blocks
    grid[2][1] = grid[2][2] = CellState.Wall
    grid[1][6] = grid[1][7] = CellState.Wall
    grid[1][4] = grid[2][4] = grid[3][4] = grid[4][4] = CellState.Wall
    grid[4][5] = grid[4][6] = CellState.Wall
    grid[4][2] = grid[5][2] = grid[6][2] = grid[7][2] = CellState.Wall
    grid[6][4] = grid[6][5] = CellState.Wall

    #set "Power position" blocks
    grid[self._powerX][self._powerY] = CellState.Power

    #set "Start Position" blocks
    grid[self._startX][self._startY] = CellState.Start

    #set "Goal" blocks
    x, y = randint(5, len(grid[0]) - 1), randint(5, len(grid[1]) - 1)
    self._goal = State(x, y)
    grid[x][y] = CellState.Goal

    return grid
  
  def nextState(self, currentState, action):
    returnState = State(currentState.x, currentState.y)
    if (action == Action.UP and currentState.x < self._rows - 1):
      returnState.x = currentState.x + 1
    elif (action == Action.Down and currentState.x > 0):
      returnState.x = currentState.x - 1
    elif (action == Action.Left and currentState.y > 0):
      returnState.y = currentState.y - 1
    elif (action == Action.Right and currentState.y < self._cols - 1):
      returnState.y = currentState.y + 1
    return returnState

  def cellState(self, state):
    return self._grid[state.x][state.y]

  def distance(self, currentState, nextState):
    return math.sqrt(((currentState.x - nextState.x)** 2) + ((currentState.y - nextState.y)** 2))

  def reached(self, state):
    return (self._goal == state)

  def action(self, currentState, action):
    '''
    If next state is open then
      cost will be euclidean distance from 
      start state to current state + current state to goal state
      and return next state
    If next state is wall then
      Its very high cost 100 and return current state only
    If next state is restart then
      cost will be euclidean distance from 
      start state to current state + start state to goal state
      and return start state
    If next state is Go to Power then
      cost will be euclidean distance from 
      start state to current state + power state to goal state
      and return power state
    '''
    nxtState = self.nextState(currentState, action)
    nxtStateValue = self.cellState(nxtState)
    
    #default Costs init for max(wall state)
    cost = 1000
    aheadCost = 0
    currCost = self.distance(self._start, currentState)
    if ((nxtStateValue == CellState.Wall) or (nxtState == currentState)):
      nxtState = currentState
      aheadCost = cost
    elif (nxtStateValue == CellState.Open or nxtStateValue == CellState.Start or nxtStateValue == CellState.Power):
      aheadCost = self.distance(currentState, self._goal)
    elif (nxtStateValue == CellState.Restart):
      aheadCost = self.distance(self._start, self._goal)
      nxtState = self._start
    elif (nxtStateValue == CellState.GOTOPower):
      aheadCost = self.distance(self._power, self._goal)
      nxtState = self._power

    cost = currCost + aheadCost
    return(nxtState, cost)
