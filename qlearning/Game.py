import tkinter as t
import pickle as p
from QLearning import Game, HumanPlayer, QPlayer

Q = p.load(open("simulation.p", "rb"))
r = t.Tk()
playerOne = HumanPlayer(sign="O")
playerTwo = QPlayer(sign="X", ep=0)
game = Game(r, playerOne, playerTwo, Q=Q)
game.play()
r.eval('tk::PlaceWindow . center')
r.mainloop()
        
