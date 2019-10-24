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
        #startTime = time.process_time()
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
            #Debugger.debug("MOVE = " + str(move))
            #while self.__board.isPlayable(move.x, move.y) == False:
            #    move.x = random.randint(0, self.__board.getSize() - 1)
            #    move.y = random.randint(0, self.__board.getSize() - 1)
        #Debugger.debug("Calculation time: " + str((time.process_time() - startTime)) + " ms")
        return move

    ##TODO
    def evaluateBoard(self, board: Board, blacksTurn: bool):
        blackScore = float(self.getScore(board, True, blacksTurn))
        whiteScore = float(self.getScore(board, False, blacksTurn))
        #Debugger.debug("----Enemy : " + str(blackScore))
        #Debugger.debug("----me : " + str(whiteScore))
        if blackScore == 0: 
            blackScore = 1.0
        return float(whiteScore / blackScore)


    def minmaxAlphaBeta(self, depth: int, board: Board, max: bool, alpha: float, beta: float):
        if depth == 0:
            #Debugger.debug("-INF-")
            value = [self.evaluateBoard(board, not max), -1, -1]
            #Debugger.debug("Min score = " + str(value[0]))
            return value
        allPossibleMoves = self.generateMoves()
        #Debugger.debug(str(allPossibleMoves))
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
                    #Debugger.debug("LOOL33")
                    return tempMove
                if float(tempMove[0]) > float(bestMove[0]):
                    #Debugger.debug("LOOL4")
                    bestMove[0] = tempMove[0]
                    bestMove[1] = move[0] 
                    bestMove[2] = move[1]
        else:
            bestMove[0] = 100000000.0#;float(self.__winScore)
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
                    #Debugger.debug("LOOL1 : " + str(tempMove))
                    return tempMove
                if float(tempMove[0]) < float(bestMove[0]):
                    #Debugger.debug("LOOL2" + str(move))
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
        ##Debugger.debug("TESTTT = " + str(movesTab))
        return movesTab

    def searchWinningMove(self):
        allPossibleMoves = self.generateMoves()
        winningMove = Vector(-1, -1)
    
    	## Iterate for all possible moves
        for move in allPossibleMoves:
            #self.__evaluationCount = self.__evaluationCount + 1
            ## Create a temporary board that is equivalent to the current board
            testBoard = copy.deepcopy(self.__board)
            ## Play the move to that temporary board without drawing anything
            #print(allPossibleMoves)
            if testBoard.isPlayable(move[0], move[1]) == False:
                continue
            testBoard.set(move[0], move[1], 1)
            #Debugger.debug("TESTBOARD : " + str(testBoard.getBoard()))
            ## If the white player has a winning score in that temporary board, return the move.
            if self.getScore(testBoard, False, False) >= self.__winScore: ##TODO check
                winningMove.x = move[0]
                winningMove.y = move[1]
                return winningMove
        return None
    
    def getConsecutiveSetScore(self, consecutive, blocks, myTurn: bool):
        winGuarantee = 1000000
        #it is not a win move
        #if consecutive > 1:
        #    Debugger.debug(str(consecutive))
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
        ##Debugger.debug("COUNT : " + str(boardM[i][j]))
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

    def evaluateVertival(self, boardM, myTurn: bool, blacksTurn: bool):
        self.__consecutive = 0
        self.__blocks = 2
        self.__score = 0

        #boardSize = len(boardM) - 1
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
        # for x in range(-1, 1):
        #     for y in range(-1, 1):
        #         if x != 0 or y != 0:
        #             score += self.evaluateDir(boardM, Vector(x, y))
        #Debugger.debug("SCORE = " + str(score))
        return score