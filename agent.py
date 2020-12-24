from enums import Action
from State import State
import random
import math

class agent:
  '''
  State-action learning will be a agent knowledge
  {
    State(0,0) : {
      Explored: {
        UP : {
          visitCount: 2,
          overallCost: 74773,
          cost: 7.88
        },
        Down : {
          visitCount: 2,
          overallCost: 74773,
          cost: 7.88
        }
      }
    }
  }
  '''
  _knowledge = {}
  _exploreWeight = .25

  _startX, _startY = 0,0
  _current = State(_startX, _startY)
  _action = [Action.UP, Action.Down, Action.Left, Action.Right]

  def reset(self):
    self._current = State(self._startX, self._startY)

  #Probality selection between exploit and explore
  def explore(self):
    return random.choices([False, True], weights=(1 - self._exploreWeight, self._exploreWeight), k=1)

  #Init stateAction for knowledge base
  def defaultState(self):
    return { 'Explored': {} }

  def action(self, currentState):
    stateAction = None
    if currentState in self._knowledge:
      stateAction = self._knowledge[currentState]
    
    isExplore = self.explore()
    if (stateAction == None):
      stateAction = self.defaultState()
      isExplore = True

    nextAction = None
    if (isExplore):
      nextAction = random.choices(self._action, k=1)[0]
    else:
      bestCost = math.inf
      for actionKey in stateAction['Explored']:
        action = stateAction['Explored'][actionKey]
        if (bestCost > action['cost']):
          bestCost = action['cost']
          nextAction = actionKey
    
    return nextAction

  def move(self, env):
    currentAction = self.action(self._current)
    nextState, actionCost = env.action(self._current, currentAction)
    
    stateKnowledge = None
    if self._current in self._knowledge:
      stateKnowledge = self._knowledge[self._current]

    if (stateKnowledge == None):
      stateKnowledge = self.defaultState()
    
    actionInfo = None
    if currentAction in stateKnowledge['Explored']:
      actionInfo = stateKnowledge['Explored'][currentAction]

    if (actionInfo == None):
      stateKnowledge['Explored'][currentAction] = { 'visitCount': 1, 'overallCost': actionCost, 'cost': actionCost }
    else:
      actionInfo['visitCount'] = actionInfo['visitCount'] + 1
      actionInfo['overallCost'] = actionInfo['overallCost'] + actionCost
      actionInfo['cost'] = actionInfo['overallCost'] / actionInfo['visitCount']
    
    self._knowledge[self._current] = stateKnowledge
    #if currentAction in self._knowledge[self._current]['Action']: 
    #  self._knowledge[self._current]['Action'].remove(currentAction)
    
    self._current = nextState
    return (currentAction, actionCost)


    

