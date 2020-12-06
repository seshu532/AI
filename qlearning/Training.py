import pickle as p
import tkinter as t
from QLearning import Game, QPlayer

r = t.Tk()
eps = 0.9
playerTwo = QPlayer(sign="X",ep = eps)
playerOne = QPlayer(sign="O",ep = eps)
g = Game(r, playerOne, playerTwo)
simulation = 200000
i = 0
while i < simulation:
    g.play()
    g.reset()
    i = i +1
Q = g.Q
name = "simulation.p".format(simulation)
p.dump(Q, open(name, "wb"))
