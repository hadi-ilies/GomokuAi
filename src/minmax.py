from board import Board
from vector import Vector
from debug import Debugger
import copy
import time
import random
class MinMax(object):
    def __init__(self, board: Board):
        self.__board = board
        self.__evaluationCount = 0
        self.__winScore = 100000000
        self.__consecutive = 0
        self.__score = 0
        self.__blocks = 2
    
    def getEvaluationCount(self):
        return self.__evaluationCount
    
    def getWinScore(self):
        return self.__winScore

    def calculateNextMove(self, depth: int):
        move = Vector(0, 0)
        startTime = time.process_time()
        bestMove = self.searchWinningMove()
        
        if bestMove != None:
            move.x = int(bestMove.x)
            move.y = int(bestMove.y)
        else:
            Debugger.debug("MINMAX")
            while self.__board.isPlayable(move.x, move.y) == False:
                move.x = random.randint(0, self.__board.getSize() - 1)
                move.y = random.randint(0, self.__board.getSize() - 1)
        Debugger.debug("Calculation time: " + str((time.process_time() - startTime)) + " ms")
        return move

    def generateMoves(self):
        movesTab = []
        boardSize = self.__board.getSize()
        board = self.__board.getBoard()
        #Look for cells that has at least one stone in an adjacent cell.

        for i in range(0, boardSize):
            for j in range(0, boardSize):
                if board[i][j] > 0: ##tmp
                    continue
                if i > 0 and j > 0:
                    if board[i - 1][j - 1] == 0 or board[i][j - 1] == 0: ## >
                        movesTab.append([i, j]) ## insert move
                        continue
                    if j < boardSize - 1:
                        if board[i - 1][j + 1] == 0 or board[i][j + 1] == 0:
                            movesTab.append([i, j]) ## insert move
                            continue
                        if board[i - 1][j] == 0:
                            movesTab.append([i, j]) ## insert move
                            continue
                if i < boardSize - 1 and j > 0:
                    if board[i + 1][j - 1] == 0 or board[i][j - 1] == 0: ## >
                        movesTab.append([i, j]) ## insert move
                        continue
                    if j < boardSize - 1:
                        if board[i + 1][j + 1] > 0 or board[i][j + 1] > 0:
                            movesTab.append([i, j]) ## insert move
                            continue
                    if board[i + 1][j] > 0:
                        movesTab.append([i, j]) ## insert move
                        continue
        return movesTab

    def searchWinningMove(self):
        allPossibleMoves = self.generateMoves()
        winningMove = Vector(0, 0)
    
    	## Iterate for all possible moves
        for move in allPossibleMoves:
            self.__evaluationCount = self.__evaluationCount + 1
            ## Create a temporary board that is equivalent to the current board
            testBoard = copy.deepcopy(self.__board)
            ## Play the move to that temporary board without drawing anything
            #print(allPossibleMoves)
            if testBoard.set(move[0], move[1], 1) == False:
                continue
            ##TODO create a getscoreFunc
            ## If the white player has a winning score in that temporary board, return the move.
            if self.getScore(testBoard) >= self.__winScore:
                winningMove.x = move[0]
                winningMove.y = move[1]
                return winningMove
        return None
    
    def getConsecutiveSetScore(self, consecutive, blocks):
        winGuarantee = 1000000
        #it is not a win move
        if blocks == 2 and consecutive < 5:
            return 0
        #you already won
        if consecutive == 5:
            return self.__winScore

        if consecutive == 4:
            if blocks == 0:
                return winGuarantee / 4
            else:
                return 200

        if consecutive == 3:
            if blocks == 0:
                return 50000
            else:
                return 10

        if consecutive == 2:
            if blocks == 0:
                return 7
            else:
                return 4

        if consecutive == 1:
            return 1
        return self.__winScore * 2

    def evaluateDir(self, boardM, i: int, j: int):
        if boardM[i][j] == 1:
	        self.__consecutive += 1
        elif boardM[i][j] == 0:
            if self.__consecutive > 0:
                self.__blocks -= 1
                self.__score += self.getConsecutiveSetScore(self.__consecutive, self.__blocks)
                self.__consecutive = 0
                self.__blocks = 1
            else:
                self.__blocks = 1
        elif self.__consecutive > 0:
            self.__score += self.getConsecutiveSetScore(self.__consecutive, self.__blocks)
            self.__consecutive = 0
            self.__blocks = 2
        else:
            self.__blocks = 2
        return

    #     boardSize = len(boardM) - 1
    #     consecutive = 0
    #     block = 2
    #     score = 0
    #     checkPos = Vector(0, 0)
    #     for i in range(0, boardSize):
    #         for j in range(0, boardSize):
    #             if boardM[i][j] == 1:
    #                 checkPos = Vector(i, j)
    #                 consecutive += 1
    #             else:
    #                 block = 1
    #             while boardM[checkPos.x][checkPos.y] == 1:
    #                 checkPos.x += vector.x
    #                 checkPos.y += vector.y
    #                 consecutive += 1
    #             consecutive -= 1
    #             if boardM[checkPos.x][checkPos.y] == 0:
    #                 block -= 1
    #                 score += self.getConsecutiveSetScore(consecutive, block)
    #                 block = 1
    #             if boardM[checkPos.x][checkPos.y] == 2:
    #                 score += self.getConsecutiveSetScore(consecutive, block)
    #                 block = 2
    #             consecutive = 0
    #     return score

    def evaluateVertival(self, boardM):
        self.__consecutive = 0
        self.__blocks = 2
        self.__score = 0

        #boardSize = len(boardM) - 1
        for j in range(0, len(boardM[0]) - 1):
            for i in range(0, len(boardM) - 1):
                self.evaluateDir(boardM, i, j)
            if self.__consecutive > 0:
                self.__score += self.getConsecutiveSetScore(self.__consecutive, self.__blocks)
            self.__consecutive = 0
            self.__blocks = 2
        score = self.__score
        self.__score = 0
        return score

    
    def evaluateHorizontal(self, boardM):
        self.__consecutive = 0
        self.__blocks = 2
        self.__score = 0

        for i in range(0, len(boardM) - 1):
            for j in range(0, len(boardM[0]) - 1):
                self.evaluateDir(boardM, i, j)
            if self.__consecutive > 0:
                self.__score += self.getConsecutiveSetScore(self.__consecutive, self.__blocks)
            self.__consecutive = 0
            self.__blocks = 2
        score = self.__score
        return score
    
    def evaluateDiagonal(self, boardM):
        self.__consecutive = 0
        self.__blocks = 2
        self.__score = 0

        ##From bottom-left to top-right diagonally
        for k in range(0, 2 * (len(boardM) - 1)):
            iStart = max(0, k - len(boardM) + 1)
            iEnd = min(len(boardM) - 1, k)
            for i in range(iStart, iEnd):
                j = k - i
                self.evaluateDir(boardM, i, j)
            if self.__consecutive > 0:
                self.__score += self.getConsecutiveSetScore(self.__consecutive, self.__blocks)
            self.__consecutive = 0
            self.__blocks = 2
        #From top-left to bottom-right diagonally
        for k in range(1 - len(boardM) - 1, len(boardM) - 1):
            iStart = max(0, k)
            iEnd = min(len(boardM) + k - 1, len(boardM) - 1)
            for i in range(iStart, iEnd):
                j = k - i
                self.evaluateDir(boardM, i, j)
            if self.__consecutive > 0:
                self.__score += self.getConsecutiveSetScore(self.__consecutive, self.__blocks)
            self.__consecutive = 0
            self.__blocks = 2
        score = self.__score
        self.__score = 0
        return score

    def getScore(self, board: Board):
        boardM = board.getBoard()
        score = self.evaluateDiagonal(boardM) + self.evaluateHorizontal(boardM) + self.evaluateVertival(boardM)
        # for x in range(-1, 1):
        #     for y in range(-1, 1):
        #         if x != 0 or y != 0:
        #             score += self.evaluateDir(boardM, Vector(x, y))
        return score