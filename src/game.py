from ai import Ai 
from protocol import protocolDir

class Game(object):
    def __init__(self):
        self.__ai = Ai()
        
    def run(self, command: list):
        protocolDir[command[0]](command[1:], self.__ai)