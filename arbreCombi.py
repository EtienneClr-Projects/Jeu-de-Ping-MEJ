import time

import numpy
import numpy as np, itertools

from algo_clics import algo

"""
ici on compte les demandes
si y'a des demandes
      si on a une demande maximale unique on clique dessus
      si on a plusieurs demandes maximales, on relance l'algo sur chaque demande
      si on a déjà cliqué à tous les endroits où y'a des demandes, on s'arrête
si y'a plus de demandes
      si on est à la dernière ligne
          si la dernière ligne est ok, on s'arrête, on affiche le tableau final
          sinon, on s'arrête
      sinon, on passe à la ligne suivante
"""

n = 4
H = n
W = n


def generate_sol_init(n):
    combs = list(set(itertools.combinations_with_replacement([0, 1, 0, 1, 0, 1], n)))
    combs_no_duplicates = []

    for i in range(len(combs)):
        combs[i] = list(combs[i])

    while len(combs) > 0:
        comb = combs.pop(0)
        if list(reversed(comb)) not in combs:
            combs_no_duplicates.append(comb)

    return combs_no_duplicates


class TABLEAU():
    def __init__(self, taille):
        self.__tableau = numpy.zeros((taille + 2, taille + 2))
        self.__taille = taille

    def get(self, x, y):
        return self.__tableau[y + 1, x + 1]

    def set(self, x, y, val=1):
        self.__tableau[y + 1, x + 1] = val

    def print_tab(self):
        print(self.__tableau[1:self.__taille + 1, 1:self.__taille + 1])

    def regarder_les_3_cases_au_dessus(self, x, y, t):
        total = 0
        if x == 0 or x == n:
            return total
        if x > 1:
            total += self.verif_impair_cases_autour(x - 1, y - 1, t)
        total += self.verif_impair_cases_autour(x, y - 1, t)
        if x < n:
            total += self.verif_impair_cases_autour(x + 1, y - 1, t)
        return total

    def verif_impair_cases_autour(self, x, y, t):
        total = 0
        if 0 < x < n + 1:
            total = np.sum(t[y - 1:y + 2, x - 1:x + 2]) - t[y, x]
        elif x == 0:
            total = np.sum(t[y - 1:y + 2, x:x + 2] - t[y, x])
        elif x == n + 1:
            total = np.sum(t[y - 1:y + 2, x - 1:x + 1])
        return (total % 2 == 0) * 1


def algo(tableau, indice_ligne_en_cours):
    """
    ici on compte les demandes
    si y'a des demandes
          si on a une demande maximale unique on clique dessus
          si on a plusieurs demandes maximales, on relance l'algo sur chaque demande
          si on a déjà cliqué à tous les endroits où y'a des demandes, on s'arrête
    si y'a plus de demandes
          si on est à la dernière ligne
              si la dernière ligne est ok, on s'arrête, on affiche le tableau final
              sinon, on s'arrête
          sinon, on passe à la ligne suivante
    """
    tableau.print_tab()
    print()


# ici on va lancer l'algo sur les x possibilités générées par generate_sol_init()
solutions_init = generate_sol_init(n)
for solution in solutions_init:
    tableau = TABLEAU(n)
    for x in range(n):
        tableau.set(1, x, solution[x])

    # on lance l'algo sur la solution
    algo(tableau, 1)
