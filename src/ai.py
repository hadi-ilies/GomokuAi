import sys
from board import Board


class Ai(object):
    def __init__(self):
        self.__board = Board(4)
        self.__x = int()
        self.__y = int()
    
    def put(self, x: int, y: int):
        self.__board.set(x, y, 1)
        self.send(str(x) + "," + str(y))

    def setBoard(self, size: int):
        self.__board = Board(size)

    def send(self, text: str):
        print(text)
        sys.stdout.flush()

    def recv(self):
        return  sys.stdin.readline().replace("\r\n", "").split(" ")

    def play(self):
        self.__x = 1
        self.__y = 2
        self.put(self.__x, self.__y)
    