from environment import *
from agent import *
import time
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--console', default='0', help='Is output on console or UI')
args = parser.parse_args()
isConsole = int(args.console)

env = environment()
agt = agent()
episodeCount = 25
lastState = State(0,0)
lastValue = "Start.png"
i = 0
currPath = 'Start'
currPathCost = 0

def timer_fn():
  global env, agt, episodeCount, lastState, lastValue, i, currPath, currPathCost
  if (episodeCount > 0):
    b[(env._rows -1) - lastState.x][lastState.y] = lastValue

    action, cost = agt.move(env)
    currPath = currPath + '->' + action.name
    currPathCost = currPathCost + cost
    lastState = agt._current
    lastValue = b[(env._rows -1) - agt._current.x][agt._current.y]
    b[(env._rows -1) - agt._current.x][agt._current.y] = "Agent.png"
    
    if (env.reached(agt._current)):
      messagebox.showinfo("Path Cost", str(currPathCost))
      messagebox.showinfo("Path followed", currPath)
      messagebox.showinfo("Knowledge Base", agt._knowledge)
      currPath = 'Start'
      currPathCost = 0
      episodeCount = episodeCount - 1
      b.pause(3000)
      agt.reset()

argCount = len(sys.argv)

if isConsole == 0:
  from tkinter import *
  from tkinter import messagebox
  from game2dboard import Board

  b = Board(8, 8)
  b.title = "RL Agent!"
  b.cell_size = (75,83)
  b[7][7] = b[2][1] = b[1][3] = "GoToPower.png"

  #set "Restart" blocks
  b[4][0] = b[4][6] = "Restart.png"

  #set "Wall" blocks
  b[5][1] = b[5][2] = "Wall.png"
  b[6][6] = b[6][7] = "Wall.png"
  b[6][4] = b[5][4] = b[4][4] = b[3][4] = "Wall.png"
  b[3][5] = b[3][6] = "Wall.png"
  b[3][2] = b[2][2] = b[1][2] = b[0][2] = "Wall.png"
  b[1][4] = b[1][5] = "Wall.png"
      
  #set "Power position" blocks
  b[(env._rows -1) - env._powerX][env._powerY] = "Power.png"

  #set "Start Position" blocks
  b[(env._rows -1) - env._startX][env._startY] = "Start.png"
  b[(env._rows -1) - env._goal.x][env._goal.y] = "Goal.png"

  b.on_timer = timer_fn
  b.start_timer(20)
  b.show()
else:
  while(episodeCount > 0):
    path = 'Start'
    while(not env.reached(agt._current)):
      action, cost = agt.move(env)
      currPath = currPath + '->' + action.name
      currPathCost = currPathCost + cost
    
    print("Path Cost: ", str(currPathCost))
    print("Path followed:", currPath)
    print("Knowledge Base: ", agt._knowledge)
    print('----')
    currPath = 'Start'
    currPathCost = 0
    agt.reset()
    episodeCount = episodeCount - 1