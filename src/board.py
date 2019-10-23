class Board(object):
    def __init__(self, size: int):
        self.__size = size
        self.__board = [[0 for _ in range(size)] for _ in range(size)]

    def getBoard(self):
        return self.__board

    def get(self, x: int, y: int):
        if x < 0 or x >= self.__size or y < 0 or y >= self.__size:
            raise ValueError("Invalid position")
        return self.__board[y][x]

    def isPlayable(self, x: int, y: int):
        if x < 0 or x >= self.__size or y < 0 or y >= self.__size:
            return False
        if self.__board[y][x] > 0:
            return False
        return True

    def set(self, x: int, y: int, value: int):
        if x < 0 or x >= self.__size or y < 0 or y >= self.__size:
            return False
            #raise ValueError("Invalid position")
        self.__board[y][x] = value
    
    def getSize(self):
        return self.__size
    
    ##i.__str__() == str(i) ??
    def str(self):
        text = str()
        for i in self.__board:
            text = text + i.__str__() + '\n'
        return text