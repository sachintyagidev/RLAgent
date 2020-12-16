from environment import *
from agent import *
from game2dboard import Board
import time

env = environment()
agt = agent()
episodeCount = 25
lastState = State(0,0)
lastValue = "Start.png"
i = 0

def timer_fn():
  global env, agt, episodeCount, lastState, lastValue, i
  if (i < 500):
    i=i+1
    return

  if (episodeCount > 0):
    b[(env._rows -1) - lastState.x][lastState.y] = lastValue

    action = agt.move(env)
    lastState = agt._current
    lastValue = b[(env._rows -1) - agt._current.x][agt._current.y]
    b[(env._rows -1) - agt._current.x][agt._current.y] = "Agent.png"
    
    if (env.reached(agt._current)):
      episodeCount = episodeCount - 1
      b.pause(3000)
      agt.reset()

b = Board(8, 8)
b.title = "RL Agent!"
b.cell_size = (75,83)

b[7][7] = b[2][1] = b[1][3] = "GOTOPower.png"

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

'''

while(episodeCount > 0):
  path = 'Start'
  while(not env.reached(agt._current)):
    path = path + '->' + (agt.move(env)).name
  print(path)
  print((agt._current.x, agt._current.y))
  agt.reset()
  print('----')
  episodeCount = episodeCount - 1
'''