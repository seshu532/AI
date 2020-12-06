import pickle as pickle
import tkinter as t
import numpy as n
import copy

class Game:
    def __init__(self, master, playerOne, playerTwo, QLearn=None, Q={}, learningRate=0.3, discountRate=0.9):
        frame = t.Frame()
        frame.grid()
        self.master = master
        master.title("Tic-Tac-Toe")
        self.playerTwo = playerTwo
        self.currentP = playerOne
        self.playerOne = playerOne
        self.nextPlayer = playerTwo
        self.emptyText = ""
        self.board = Board()
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        for index in range(3):
            for col in range(3):
                self.buttons[index][col] = t.Button(frame, height=6, width=6, text=self.emptyText, highlightbackground='#F0F8FF', foreground = "red", command=lambda index=index, col=col: self.callback(self.buttons[index][col]))
                self.buttons[index][col].grid(row=index, column=col)
        self.resetButton = t.Button(text="Restart",  width=20, highlightbackground='#F0F8FF', foreground = "red", command=self.reset)
        self.resetButton.grid(row=3)
        self.QLearn = QLearn
        if self.QLearn:
            self.Q = Q
            self.learningRate = learningRate
            self.discountRate = discountRate
            self.share()

    @property
    def QLearn(self):
        if self._QLearn is not None:
            return self._QLearn
        if isinstance(self.playerOne, QPlayer) or isinstance(self.playerTwo, QPlayer):
            return True

    @QLearn.setter
    def QLearn(self, _QLearn):
        self._QLearn = _QLearn

    def share(self):
        if isinstance(self.playerOne, QPlayer):
            self.playerOne.Q = self.Q
        if isinstance(self.playerTwo, QPlayer):
            self.playerTwo.Q = self.Q

    def callback(self, button):
        if self.board.over():
            pass
        else:
            if isinstance(self.currentP, HumanPlayer) and isinstance(self.nextPlayer, HumanPlayer):
                if self.empty(button):
                    move = self.getMove(button)
                    self.handleMove(move)
            elif isinstance(self.currentP, HumanPlayer) and isinstance(self.nextPlayer, PlayerMachine):
                playerComputer = self.nextPlayer
                if self.empty(button):
                    humanAction = self.getMove(button)
                    self.handleMove(humanAction)
                    if not self.board.over():
                        computerAction = playerComputer.getMove(self.board)
                        self.handleMove(computerAction)

    def empty(self, button):
        return button["text"] == self.emptyText

    def getMove(self, button):
        info = button.grid_info()
        move = (int(info["row"]), int(info["column"]))
        return move

    def handleMove(self, move):
        if self.QLearn:
            self.learnQ(move)
        i, j = move
        self.buttons[i][j].configure(text=self.currentP.sign)
        self.board.placeSign(move, self.currentP.sign)
        if self.board.over():
            self.returnOutcome()
        else:
            self.switchPlayers()

    def returnOutcome(self):
        if self.board.winner() is None:
            print("Tie game.")
        else:
            print(("Player {sign} wins! Game Over!".format(sign=self.currentP.sign)))

    def reset(self):
        print("Restarting another round...")
        for row in range(3):
            for col in range(3):
                self.buttons[row][col].configure(text=self.emptyText)
        self.board = Board(grid=n.ones((3,3))*n.nan)
        self.nextPlayer = self.playerTwo
        self.currentP = self.playerOne
        self.play()

    def switchPlayers(self):
        if self.currentP == self.playerTwo:
            self.nextPlayer = self.playerTwo
            self.currentP = self.playerOne
        else:
            self.nextPlayer = self.playerOne
            self.currentP = self.playerTwo
            
           

    def play(self):
        if isinstance(self.playerOne, HumanPlayer) and isinstance(self.playerTwo, HumanPlayer):
            pass
        elif isinstance(self.playerOne, HumanPlayer) and isinstance(self.playerTwo, PlayerMachine):
            pass
        elif isinstance(self.playerOne, PlayerMachine) and isinstance(self.playerTwo, HumanPlayer):
            computerAct = playerOne.getMove(self.board)
            self.handleMove(computerAct)
        elif isinstance(self.playerOne, PlayerMachine) and isinstance(self.playerTwo, PlayerMachine):
            while not self.board.over():
                self.playNextTurn()

    def playNextTurn(self):
        move = self.currentP.getMove(self.board)
        self.handleMove(move)

    def learnQ(self, move):
        stateKey = QPlayer.createKey(self.board, self.currentP.sign, self.Q)
        nextBoard = self.board.getNextBoard(move, self.currentP.sign)
        reward = nextBoard.dishReward()
        nextStateKey = QPlayer.createKey(nextBoard, self.nextPlayer.sign, self.Q)
        if nextBoard.over():
            expected = reward
        else:
            next_Qs = self.Q[nextStateKey]
            if self.currentP.sign == "X":
                expected = reward + (self.discountRate * min(next_Qs.values()))
            elif self.currentP.sign == "O":
                expected = reward + (self.discountRate * max(next_Qs.values()))
        change = self.learningRate * (expected - self.Q[stateKey][move])
        self.Q[stateKey][move] += change


class Board:
    def __init__(self, grid=n.ones((3,3))*n.nan):
        self.grid = grid

    def winner(self):
        rows = [self.grid[row,:] for row in range(3)]
        columns = [self.grid[:,col] for col in range(3)]
        diag = [n.array([self.grid[row,row] for row in range(3)])]
        crossDiagonal = [n.array([self.grid[2-rm,rm] for rm in range(3)])]
        lanes = n.concatenate((rows, columns, diag, crossDiagonal))

        anyLane = lambda x: any([n.array_equal(lane, x) for lane in lanes])
        if anyLane(n.zeros(3)):
            return "O"
        elif anyLane(n.ones(3)):
            return "X"

    def over(self):
        return (not n.any(n.isnan(self.grid))) or (self.winner() is not None)

    def placeSign(self, move, sign):
        num = Board.signToNumber(sign)
        self.grid[tuple(move)] = num

    @staticmethod
    def signToNumber(sign):
        d = {"X": 1, "O": 0}
        return d[sign]

    def availableMoves(self):
        return [(i,j) for i in range(3) for j in range(3) if n.isnan(self.grid[i][j])]

    def getNextBoard(self, move, sign):
        nextBoard = copy.deepcopy(self)
        nextBoard.placeSign(move, sign)
        return nextBoard

    def generateKey(self, sign):
        val = 9
        filledGrid = copy.deepcopy(self.grid)
        n.place(filledGrid, n.isnan(filledGrid), val)
        return "".join(map(str, (list(map(int, filledGrid.flatten()))))) + sign

    def dishReward(self):
        if self.over():
            if self.winner() is not None:
                if self.winner() == "O":
                    return 1.0
                elif self.winner() == "X":
                    return -1.0
            else:
                return 0.5
        else:
            return 0.0


class Player(object):
    def __init__(self, sign):
        self.sign = sign

class HumanPlayer(Player):
    pass

class PlayerMachine(Player):
    pass

class QPlayer(PlayerMachine):
    def __init__(self, sign, Q={}, ep=0.2):
        super(QPlayer, self).__init__(sign=sign)
        self.Q = Q
        self.ep = ep

    @staticmethod
    def randArgMinMax(Qs, minMax):
        minMaxQ = minMax(list(Qs.values()))
        if list(Qs.values()).count(minMaxQ) > 1:
            perfectOptions = [move for move in list(Qs.keys()) if Qs[move] == minMaxQ]
            move = perfectOptions[n.random.choice(len(perfectOptions))]
        else:
            move = minMax(Qs, key=Qs.get)
        return move
    
    def getMove(self, board):
        if n.random.uniform() < self.ep:
            return RandPlayer.getMove(board)
        else:
            stateKey = QPlayer.createKey(board, self.sign, self.Q)
            Qs = self.Q[stateKey]

            if self.sign == "O":
                return QPlayer.randArgMinMax(Qs, max)
            elif self.sign == "X":
                return QPlayer.randArgMinMax(Qs, min)

    @staticmethod
    def createKey(board, sign, Q):
        default = 1.0
        stateKey = board.generateKey(sign)
        if Q.get(stateKey) is None:
            moves = board.availableMoves()
            Q[stateKey] = {move: default for move in moves}
        return stateKey

class RandPlayer(PlayerMachine):
    @staticmethod
    def getMove(board):
        moves = board.availableMoves()
        if moves:
            return moves[n.random.choice(len(moves))]


    
