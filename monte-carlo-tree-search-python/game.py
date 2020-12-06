"""
Developed by Seshaiah Erugu & Krikor Herlopian
Simple Monte Carlo AI.
You will play against a computer when you run this application.

The board looks as below.
0 1 2
3 4 5
6 7 8

Just as an example this means
X O -
X - O
X - -
the following tuple:
(True, False, None, True, None, False, True, None, None)

None means empty. True means X, False means O.
"""

from mcts import MonteCarloTreeSearch, Node
from random import choice
from collections import namedtuple

ticTacToeB = namedtuple("MonteCarloAITicTacToeBoard", "tuple victorious turn leaf")


class GameBoard(ticTacToeB, Node):
    def findChildren(board):
                    
        #make a move in each of the empty spots
        if not board.leaf:
            return {
             board.makeMove(a)
             for a, val in enumerate(board.tuple) if val is None
            }
        else:  # the game is finished, no move to be made.
            return set()
        

    def findRandomChild(board):
        if not board.leaf:
            openSpots = [a for a, b in enumerate(board.tuple) if b is None]
            return board.makeMove(choice(openSpots))
        return None  #  the game is over.
        

    def reward(board):
        if not board.leaf:
            raise RuntimeError(f"reward called on nonleaf board {board}")
        if board.victorious is board.turn:
            # You won, its your turn.
            raise RuntimeError(f"reward called on unreachable board {board}")
        if board.victorious is None:
            return 0.5  # 0.5 means the board is a tie
        if board.turn is (not board.victorious):
            return 0  # 0 here will mean that the opponent just won.
        #  Unknown result. No true or false or none
        raise RuntimeError(f"board has unknown winner type {board.victorious}")

    def isLeaf(board):
        return board.leaf

    def makeMove(board, index):
        tuple = board.tuple[:index] + (board.turn,) + board.tuple[index + 1 :]
        turn = not board.turn
        victorious = findWinner(tuple)
        isLeaf = (victorious is not None) or not any(v is None for v in tuple)
        return GameBoard(tuple, victorious, turn, isLeaf)
        
    def toString(board):
        value = "\n\n"
        value += toChar(board.tuple[0]) + "  | " + toChar(board.tuple[1]) + " | " + toChar(board.tuple[2])
        value += "\n-----------\n"
        value += toChar(board.tuple[3]) + "  | " + toChar(board.tuple[4]) + " | " + toChar(board.tuple[5])
        value += "\n-----------\n"
        value += toChar(board.tuple[6]) + "  | " + toChar(board.tuple[7]) + " | " + toChar(board.tuple[8])
        value += "\n\n"
        return value
    

def findWinner(tuple):
    "It will return true if X wins, None if there is no winner. When O wins it will return false"
    for i, j, k in winningScenarios():
        a, b, c = tuple[i], tuple[j], tuple[k]
        if False is a is b is c:
            return False
        if True is a is b is c:
            return True
    return None

def play():
    tree = MonteCarloTreeSearch()
    board = newBoard()
    print(board.toString())
    while True:
        rowColumn = input("enter in this format row,col: ")
        row, col = map(int, rowColumn.split(","))
        index = 3 * (row - 1) + (col - 1)
        if board.tuple[index] is not None:
            raise RuntimeError("Invalid move")
        board = board.makeMove(index)
        print(board.toString())
        if board.leaf:
            break
        # You can train at every round, or you can handle training only at the begining.
        # We are currently training as we move by each round, every round 2500 rollouts.
        # the more we increase number, the tough we win.If we decrease this to 30 rollouts winning becomes far easier.
        for _ in range(2500):
            tree.makeRollout(board)
        board = tree.choose(board)
        print(board.toString())
        if board.leaf:
            break

def toChar(v):
    if v:
        return "X"
    if v is False:
        return "O"
    return " "

def winningScenarios():
    yield (2, 4, 6) # diagonal win
    yield (0, 4, 8) # diagonal win.
    for i in range(3):
        yield (i, i + 3, i + 6) # vertically won
    for k in range(0, 9, 3):
        yield (k, k + 1, k + 2) # horizontally won.

def newBoard():
    return GameBoard(tuple=(None,) * 9, victorious=None, turn=True,  leaf=False)

if __name__ == "__main__":
    play()


    

