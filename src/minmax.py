from board import Board

class MinMax(object):
    def __init__(self, board: Board):
        self.__board = board
        self.__evaluationCount = 0
        self.__winScore = 100000000
    
    def getEvaluationCount(self):
        return self.__evaluationCount
    
    def getWinScore(self):
        return self.__winScore

    def generateMoves(self):
        movesTab = [[]]
        boardSize = self.__board.getSize()
        board = self.__board.getBoard()
        #Look for cells that has at least one stone in an adjacent cell.

        for i in range(0, boardSize):
            for j in range(0, boardSize):
                if board[i][j] == 0: ##tmp
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
        winningMove = []
    
    	## Iterate for all possible moves
        for move in allPossibleMoves:
            self.__evaluationCount = self.__evaluationCount + 1
            ## Create a temporary board that is equivalent to the current board
            testBoard = self.__board.copyBoard()
            ## Play the move to that temporary board without drawing anything
            if testBoard.set(move[0], move[1], 1) == False:
                continue
            ##TODO create a getscoreFunc
            ## If the white player has a winning score in that temporary board, return the move.
            if self.getScore(testBoard) >= self.__winScore:
                winningMove[0] = move[0]
                winningMove[1] = move[1]
                return winningMove
        return None
    
    def evaluateDiagonal(self, boardM):
        return 1
    def evaluateHorizontal(self, boardM):
        return 2
    def evaluateVertical(self, boardM):
        return 3

    def getScore(self, board: Board):
        boardM = board.getBoard()
        score = self.evaluateHorizontal(boardM) + self.evaluateVertical(boardM) + self.evaluateDiagonal(boardM)
        return score