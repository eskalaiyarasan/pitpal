from abc import ABC, abstractmethod
from enum import Enum

class State(Enum):
    NEW= 1
    READY = 2
    WAIT = 3
    RUN = 4
    PAUSE = 5
    BLOCK = 6
    STOP = 6
    GAMEOVER = 7
    UNKNOWN = 0
  
class baseboard():
  def __init__(self):
    self.state = State.NEW
    
  @abstractmethod
  def move(self,index):
    if self.state != State.RUN:
      return False
    return True
    
  def isGameOver(self):
    if self.state == State.GAMEOVER:
      return True
    return False
    
  @abstractmethod
  def repr(self):
    pass
    
