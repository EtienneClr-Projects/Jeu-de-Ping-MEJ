import numpy as np
import random, operator, copy, time, math
import matplotlib.pyplot as plt
from itertools import *

"""
l'ordre n'a pas d'importance
2 fois la même position annule quelque soit le moment, donc on ne clique pas 2 fois au même endroit
on arrive pas à résoudre un 3x3 ou 5x5 ou 7x7
en fait notre méthode de tri par ordre de score est peut-etre mauvaise
c'est pas parce qu'on a un bon score qu'on tend vers le tableau complet
"""


class PLATEAU():
    def __init__(self):
        self.tableau = np.zeros((H, W))

    def jouer_sequence(self, positions_seq):
        for position in positions_seq:
            self.cliquer(position[0], position[1])

    def cliquer(self, x, y):
        if (x != 0 and y != 0):  # en haut à gauche
            self.tableau[x - 1, y - 1] = not self.tableau[x - 1, y - 1]
        if (y != 0):  # milieu haut
            self.tableau[x, y - 1] = not self.tableau[x, y - 1]
        if (x != n - 1 and y != 0):  # haut droit
            self.tableau[x + 1, y - 1] = not self.tableau[x + 1, y - 1]
        if (x != n - 1):  # gauche milieu
            self.tableau[x + 1, y] = not self.tableau[x + 1, y]
        if (x != n - 1 and y != n - 1):  # bas droite
            self.tableau[x + 1, y + 1] = not self.tableau[x + 1, y + 1]
        if (y != n - 1):  # milieu bas
            self.tableau[x, y + 1] = not self.tableau[x, y + 1]
        if (y != n - 1 and x != 0):  # bas gauche
            self.tableau[x - 1, y + 1] = not self.tableau[x - 1, y + 1]
        if (x != 0):  # milieu gauche
            self.tableau[x - 1, y] = not self.tableau[x - 1, y]

    def evaluer(self):
        return np.sum(self.tableau)


n = 4
H = n
W = n
MAX = n * n
clics = 40
"""
T = list(range(n)) + list(range(n))
positions_possibles = list(set(combinations_with_replacement(T, 2)))
print(positions_possibles)
combinaisons_possibles = list(combinations_with_replacement(positions_possibles, clics)) + list(combinations_with_replacement(positions_possibles, clics))
print(combinaisons_possibles)
#combinaisons_possibles = [((1,1),(0,0),(1,2),(0,3),(2,0),(2,3))]
#print(combinaisons_possibles)
print(len(combinaisons_possibles))
"""
"""
T = list(range(n)) + list(range(n))
print(T)
positions_possibles = list(set(combinations_with_replacement(T,2)))
#print(positions_possibles)
combinaisons_possibles = list(set(combinations_with_replacement(positions_possibles, clics)))
print(combinaisons_possibles)
print(len(combinaisons_possibles))

for combi in combinaisons_possibles:
	plateau = PLATEAU()
	plateau.jouer_sequence(combi)
	score = plateau.evaluer()
	#print(score)
	if score==MAX:
		break

print("score : ", score)
print(plateau.tableau)
"""
tab = []
with open('test seq.txt') as file:
	lines = file.readlines()
	for line in lines:
		tab.append(tuple(map(int,line[1:-2].split(","))))

print(tab)
print("len :",len(tab))
plateau = PLATEAU()
plateau.jouer_sequence(tab)
print("score :",plateau.evaluer())
print(plateau.tableau)