from debug import Debug
from ai import Ai 
from protocol import protocolDir

class Game(object):
    def __init__(self):
        self.__debugger = Debug()
        self.__ai = Ai()
    
    def getDebugger(self):
        return self.__debugger
    
    def run(self, command: list):
        protocolDir[command[0]](command[1:], self.__ai)