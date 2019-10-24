import sys
from board import Board
from minmax import MinMax
import random

class Ai(object):
    def __init__(self):
        self.__board = Board(19)
        self.__x = int()
        self.__y = int()
        self.__maxDepth = 2
        self.__minmax = MinMax(self.__board)

    ##stoneOwner 1 is our stone 2 is the enemy stone 
    def put(self, x: int, y: int):
        self.__board.set(x, y, 1)
        self.send(str(x) + "," + str(y))

    def getBoard(self):
        return self.__board

    def setBoard(self, size: int):
        self.__board = Board(size)
        self.__minmax = MinMax(self.__board)

    def send(self, text: str):
        print(text)
        sys.stdout.flush()

    def recv(self):
        return input().replace("\r", "").replace("\n", "").split(" ")

    def firstPlay(self):
        self.__x = int(self.__board.getSize() / 2)
        self.__y = int(self.__board.getSize() / 2)
        self.put(self.__x, self.__y)
    
    def play(self, xEnemy: int, yEnemy: int):
        ## todo change this shit soon as you can
        move = self.__minmax.calculateNextMove(self.__maxDepth)
        self.put(move.x, move.y)

    