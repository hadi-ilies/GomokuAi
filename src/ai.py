import sys
from board import Board
import random

class Ai(object):
    def __init__(self):
        self.__board = Board(4)
        self.__x = int()
        self.__y = int()
    
    ##stoneOwner 1 is our stone 2 is the enemy stone 
    def put(self, x: int, y: int):
        self.__board.set(x, y, 1)
        self.send(str(x) + "," + str(y))

    def getBoard(self):
        return self.__board

    def setBoard(self, size: int):
        self.__board = Board(size)

    def send(self, text: str):
        print(text)
        sys.stdout.flush()

    def recv(self):
        return input().replace("\r", "").replace("\n", "").split(" ")

    def firstPlay(self):
        self.__x = random.randint(0, self.__board.getSize() - 1)
        self.__y = random.randint(0, self.__board.getSize() - 1)
        self.put(self.__x, self.__y)
    
    def play(self, xEnemy: int, yEnemy: int):
        ## todo change this shit soon as you can
        x = -1
        y = -1
        while (self.__board.isPlayable(x, y) == False):
            x = random.randint(0, self.__board.getSize() - 1)
            y = random.randint(0, self.__board.getSize() - 1)
        # Bof go mettre une ia
        self.put(x, y)

    