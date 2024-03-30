import numpy as np
import random, operator, copy, time, math
import matplotlib.pyplot as plt
from itertools import combinations_with_replacement

"""
l'ordre n'a pas d'importance
2 fois la même position annule quelque soit le moment, donc on ne clique pas 2 fois au même endroit
on arrive pas à résoudre un 3x3 ou 5x5 ou 7x7
en fait notre méthode de tri par ordre de score est peut-etre mauvaise
c'est pas parce qu'on a un bon score qu'on tend vers le tableau complet


bonjour je vais vous parler des nyctalope
	les nyctalopes ce ne sont pas des grosses putes comme on pourrait le penser
	en fait cest la capacité de voir dans le noir de certains animaux
	par exemple on peut dire que les chats sont des nyctalopes mais on peut aussi dire que ce sont des 

"""
n = 10
H = n
W = n
MAX = n * n
clics = 16


class PLATEAU():
    def __init__(self):
        self.clics = np.zeros((H + 2, W + 2))
        self.tableau = np.zeros((H + 2, W + 2))  # todo c'est uniquement pour la première ligne grisée

    def jouer_sequence(self, positions_seq):
        for position in positions_seq:
            self.cliquer(position[0], position[1])

    def cliquer(self, x, y):
        # todo pareil
        x += 1
        y += 1
        self.clics[x, y] = 1

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

    def compter_clics_voisins_case(self, x, y):
        t = self.clics
        return t[x - 1, y - 1] + t[x - 1, y] + t[x - 1, y + 1] + t[x, y + 1] + t[x, y - 1] + t[x + 1, y + 1] + t[
            x + 1, y] + t[x + 1, y - 1]

    def jouer(self):
        print("\n ETAPE 1 \n")
        self.cliquer(0, 0)
        self.cliquer(2, 0)
        self.cliquer(3, 0)
        self.cliquer(4, 0)
        # symétrique |
        self.cliquer(5, 0)
        self.cliquer(6, 0)
        self.cliquer(7, 0)
        self.cliquer(9, 0)

        self.cliquer(0, 2)
        self.cliquer(0, 3)
        self.cliquer(0, 4)
        # symétrique -
        self.cliquer(0, 5)
        self.cliquer(0, 6)
        self.cliquer(0, 7)
        self.cliquer(0, 9)

        print(self.clics)

        print("\n ETAPE 2 \n")
        for x in range(1, H):
            for y in range(1, W):
                c = self.compter_clics_voisins_case(x - 1, y - 1)
                if ((c % 2) == 0):
                    self.cliquer(x, y)
                # self.tableau[x,y] = ((c%2)==0)


debut = time.time()

plateau = PLATEAU()
plateau.jouer()
print(plateau.clics)
print("temps total : ", time.time() - debut)
