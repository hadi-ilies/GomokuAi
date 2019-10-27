from board import Board
from vector import Vector
from debug import Debugger
import copy
import time
import random
class MinMax(object):
    def __init__(self, board: Board):
        self.__board = board ##copy.deepcopy(board)
        self.__evaluationCount = 0
        self.__winScore = 100000000
        self.__consecutive = 0
        self.__score = 0
        self.__blocks = 2
        self.lol = 0
    
    def getEvaluationCount(self):
        return self.__evaluationCount
    
    def getWinScore(self):
        return self.__winScore

    def calculateNextMove(self, depth: int):
        move = Vector(-1, -1)
        bestMove = self.searchWinningMove()
        
        if bestMove != None:
            move.x = bestMove.x
            move.y = bestMove.y
        else:
            Debugger.debug("MINMAX")
            tempMove = self.minmaxAlphaBeta(depth, self.__board, True, -1.0, float(self.__winScore))
            move = Vector(tempMove[1], tempMove[2])
            Debugger.debug("DEBUG")
            self.evaluateBoard(self.__board, True)
        return move

    ##TODO
    def evaluateBoard(self, board: Board, blacksTurn: bool):
        blackScore = float(self.getScore(board, True, blacksTurn))
        whiteScore = float(self.getScore(board, False, blacksTurn))
        if blackScore == 0: 
            blackScore = 1.0
        return float(whiteScore / blackScore)


    def minmaxAlphaBeta(self, depth: int, board: Board, max: bool, alpha: float, beta: float):
        if depth == 0:
            value = [self.evaluateBoard(board, not max), -1, -1]
            return value
        allPossibleMoves = self.generateMoves()
        if len(allPossibleMoves) == 0:
            value = [self.evaluateBoard(board, not max), -1, -1]
            return value
        bestMove = [-1] * 3
        if max == True:
            bestMove[0] = -1.0
            # 	// Iterate for all possible moves that can be made.
            for move in allPossibleMoves:
                ## Create a temporary board that is equivalent to the current board
                testBoard = copy.deepcopy(board)
                #Debugger.debug(str(move))
                if testBoard.isPlayable(move[0], move[1]) == False:
                    continue
                testBoard.set(move[0], move[1], 1)
                ## Call the minimax function for the next depth, to look for a minimum score.
                tempMove = self.minmaxAlphaBeta(depth - 1, testBoard, not max, alpha, beta)
                # Updating alpha
                if float(tempMove[0]) > alpha:
                    alpha = float(tempMove[0])
                ##Pruning with beta
                if float(tempMove[0]) >= beta:
                    return tempMove
                if float(tempMove[0]) > float(bestMove[0]):
                    bestMove[0] = tempMove[0]
                    bestMove[1] = move[0] 
                    bestMove[2] = move[1]
        else:
            bestMove[0] = float(self.__winScore)
            bestMove[1] = allPossibleMoves[0][0]
            bestMove[2] = allPossibleMoves[0][1]
            for move in allPossibleMoves:
                ## Create a temporary board that is equivalent to the current board
                testBoard = copy.deepcopy(board)
                if testBoard.isPlayable(move[0], move[1]) == False:
                    continue
                testBoard.set(move[0], move[1], 2)
                ## Call the minimax function for the next depth, to look for a minimum score.
                tempMove = self.minmaxAlphaBeta(depth - 1, testBoard, not max, alpha, beta)
                # Updating beta
                if float(tempMove[0]) < beta:
                    beta = float(tempMove[0])
                ##Pruning with alpha
                if float(tempMove[0]) <= alpha:
                    return tempMove
                if float(tempMove[0]) < float(bestMove[0]):
                    bestMove[0] = tempMove[0]
                    bestMove[1] = move[0]
                    bestMove[2] = move[1]
        return bestMove

    def generateMoves(self):
        movesTab = []
        boardSize = self.__board.getSize()
        board = self.__board.getBoard()
        #Look for cells that has at least one stone in an adjacent cell.
        for i in range(0, boardSize):
            for j in range(0, boardSize):
                if board[i][j] > 0: ##tmp
                    continue
                if i > 0:
                    if j > 0:
                        if board[i - 1][j - 1] > 0 or board[i][j - 1] > 0: ## >
                            movesTab.append([i, j]) ## insert move
                            continue
                    if j < boardSize - 1:
                        if board[i - 1][j + 1] > 0 or board[i][j + 1] > 0:
                            movesTab.append([i, j]) ## insert move
                            continue
                    if board[i - 1][j] > 0:
                        movesTab.append([i, j]) ## insert move
                        continue
                if i < boardSize - 1:
                    if j > 0:
                        if board[i + 1][j - 1] > 0 or board[i][j - 1] > 0: ## >
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
        winningMove = Vector(-1, -1)
    
    	## Iterate for all possible moves
        for move in allPossibleMoves:
            ## Create a temporary board that is equivalent to the current board
            testBoard = copy.deepcopy(self.__board)
            ## Play the move to that temporary board without drawing anything
            if testBoard.isPlayable(move[0], move[1]) == False:
                continue
            testBoard.set(move[0], move[1], 1)
            ## If the white player has a winning score in that temporary board, return the move.
            if self.getScore(testBoard, False, False) >= self.__winScore: ##TODO check
                winningMove.x = move[0]
                winningMove.y = move[1]
                return winningMove
        return None
    
    def getConsecutiveSetScore(self, consecutive, blocks, myTurn: bool):
        winGuarantee = 1000000
        #it is not a win move
        if blocks == 2 and consecutive < 5:
            return 0
        #you already won
        if consecutive == 5:
            return self.__winScore

        if consecutive == 4:
            if myTurn:
                return winGuarantee
            else:
                if blocks == 0:
                    return winGuarantee / 4
                else:
                    return 200

        if consecutive == 3:
            if blocks == 0:
                if myTurn:
                    return 50000
                else:
                    return 200
            else:
                if myTurn:
                    return 10
                else:
                   return 5
        if consecutive == 2:
            if blocks == 0:
                if myTurn:
                    return 7
                else:
                    return 5
            else:
                return 3
        if consecutive == 1:
            return 1
        return self.__winScore * 2
    def evaluateDir(self, boardM, i: int, j: int, myTurn: bool, blacksTurn: bool):
        owner = 1
        if myTurn:
            owner = 2
        else:
            owner = 1
        if boardM[i][j] == owner:
            self.__consecutive = self.__consecutive + 1
        elif boardM[i][j] == 0:
            if self.__consecutive > 0:
                self.__blocks -= 1
                self.__score += self.getConsecutiveSetScore(self.__consecutive, self.__blocks, blacksTurn == myTurn)
                self.__consecutive = 0
                self.__blocks = 1
            else:
                self.__blocks = 1
        elif self.__consecutive > 0:
            self.__score += self.getConsecutiveSetScore(self.__consecutive, self.__blocks, blacksTurn == myTurn)
            self.__consecutive = 0
            self.__blocks = 2
        else:
            self.__blocks = 2

    def evaluateVertival(self, boardM, myTurn: bool, blacksTurn: bool):
        self.__consecutive = 0
        self.__blocks = 2
        self.__score = 0

        for i in range(0, len(boardM) - 1):
            for j in range(0, len(boardM[0]) - 1):
                self.evaluateDir(boardM, i, j, myTurn, blacksTurn)
            if self.__consecutive > 0:
                self.__score += self.getConsecutiveSetScore(self.__consecutive, self.__blocks, blacksTurn == myTurn)
            self.__consecutive = 0
            self.__blocks = 2
        score = self.__score
        return score

    
    def evaluateHorizontal(self, boardM, myTurn: bool, blacksTurn: bool):
        self.__consecutive = 0
        self.__blocks = 2
        self.__score = 0

        for j in range(0, len(boardM[0]) - 1):
            for i in range(0, len(boardM) - 1):
                self.evaluateDir(boardM, i, j, myTurn, blacksTurn)
            if self.__consecutive > 0:
                self.__score += self.getConsecutiveSetScore(self.__consecutive, self.__blocks, blacksTurn == myTurn)
            self.__consecutive = 0
            self.__blocks = 2
        score = self.__score
        return score
    
    def evaluateDiagonal(self, boardM, myTurn: bool, blacksTurn: bool):
        self.__consecutive = 0
        self.__blocks = 2
        self.__score = 0

        ##From bottom-left to top-right diagonally
        for k in range(0, 2 * (len(boardM) - 1)):
            iStart = max(0, k - len(boardM) + 1)
            iEnd = min(len(boardM) - 1, k)
            for i in range(iStart, iEnd):
                j = k - i
                self.evaluateDir(boardM, i, j, myTurn, blacksTurn)
            if self.__consecutive > 0:
                self.__score += self.getConsecutiveSetScore(self.__consecutive, self.__blocks, blacksTurn == myTurn)
            self.__consecutive = 0
            self.__blocks = 2
        #From top-left to bottom-right diagonally
        for k in range(1 - len(boardM) - 1, len(boardM) - 1):
            iStart = max(0, k)
            iEnd = min(len(boardM) + k - 1, len(boardM) - 1)
            for i in range(iStart, iEnd):
                j = i - k
                self.evaluateDir(boardM, i, j, myTurn, blacksTurn)
            if self.__consecutive > 0:
                self.__score += self.getConsecutiveSetScore(self.__consecutive, self.__blocks, blacksTurn == myTurn)
            self.__consecutive = 0
            self.__blocks = 2
        score = self.__score
        return score

    def getScore(self, board: Board, myturn: bool, blacksTurn: bool):
        boardM = board.getBoard()
        score = self.evaluateHorizontal(boardM, myturn, blacksTurn) + self.evaluateVertival(boardM, myturn, blacksTurn) + self.evaluateDiagonal(boardM, myturn, blacksTurn)
        return score