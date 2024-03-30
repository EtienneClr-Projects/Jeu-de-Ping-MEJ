import itertools
import time

import numpy
import numpy as np

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

n = 6
H = n
W = n
SOLUTIONS_TROUVEES = []


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
    def __init__(self, taille, tab=None):
        if tab is None:
            self.__tableau = numpy.zeros((taille + 2, taille + 2))
        else:
            self.__tableau = tab
        self.__taille = taille

    def get(self, x, y):
        return self.__tableau[y + 1, x + 1]

    def set(self, x, y, val=1):
        self.__tableau[y + 1, x + 1] = val

    def print_tab(self):
        print(self.__tableau[1:self.__taille + 1, 1:self.__taille + 1])

    def copy_tab(self):
        return self.__tableau.copy()

    def compter_demandes_pour_ligne(self, y):
        demandes_sur_ligne = []
        for i in range(0, n):
            demandes_sur_ligne.append(self.compter_demandes_pour_case(i, y - 1))
        return demandes_sur_ligne

    def compter_demandes_pour_case(self, x, y):
        total = 0
        if x > 0:
            total += self.verif_impair_cases_autour(x - 1, y)
        total += self.verif_impair_cases_autour(x, y)
        if x < n - 1:
            total += self.verif_impair_cases_autour(x + 1, y)
        return total

    def verif_impair_cases_autour(self, x, y):
        """
        retourne 1 si le nombre de cases cliquées autour est
        :param x:
        :param y:
        :return:
        """
        x += 1  # pour se replacer par rapport aux bordures
        y += 1
        total = 0
        if 0 < x < n + 1:
            total = np.sum(self.__tableau[y - 1:y + 2, x - 1:x + 2]) - self.__tableau[y, x]
        elif x == 0:
            total = np.sum(self.__tableau[y - 1:y + 2, x:x + 2] - self.__tableau[y, x])
        elif x == n + 1:
            total = np.sum(self.__tableau[y - 1:y + 2, x - 1:x + 1])
        # print("autour de ", x, y, ":", total)
        if total < 0:
            print("ERREUUUUR")
            return None
        return (total % 2 == 0) * 1


def algo(tableau, indice_ligne_en_cours, nom, nombre_de_resolus, dernier_endroit_clique):
    # if tableau.get(1, 1) == 1 and tableau.get(0, 1) == 0 and tableau.get(0, 2) == 0 and tableau.get(0,3)==0 and tableau.get(0,4)==0:
    # print("OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO")
    # tableau.print_tab()
    # print("\n")
    # time.sleep(0.1)
    # print("\n", nom)

    # ici on compte les demandes pour la ligne au dessus
    demandes_sur_cette_ligne = tableau.compter_demandes_pour_ligne(indice_ligne_en_cours)
    # print(demandes_sur_cette_ligne)

    # si y'a des demandes
    val_max = max(demandes_sur_cette_ligne)
    if val_max > 0:
        # si on a déjà cliqué à tous les endroits où y'a des demandes, on s'arrête
        somme = 0
        for i in range(n):
            somme += ((tableau.get(i, indice_ligne_en_cours) + 1) % 2) * demandes_sur_cette_ligne[i]
        if somme == 0:  # on a déjà cliqué partout
            return
        else:
            # si on a une demande maximale unique on clique dessus
            nb_demandes_max = demandes_sur_cette_ligne.count(val_max)
            if nb_demandes_max == 1: #todo c'était 0 avant bizarre ? mais y'a un bogue maintenant
                tableau.set(demandes_sur_cette_ligne.index(val_max), indice_ligne_en_cours)
                algo(tableau, indice_ligne_en_cours, nom[:-1] + str(indice_ligne_en_cours), nombre_de_resolus,
                     dernier_endroit_clique)
                return
            else:
                # si on a plusieurs demandes maximales, on relance l'algo sur chaque demande en cliquant dessus avant
                for i in range(n):
                    if demandes_sur_cette_ligne[i] != 0 \
                            and tableau.get(i, indice_ligne_en_cours) == 0:  # todo @andre j'ai essayé ca
                        tableau_duplique = TABLEAU(n, tableau.copy_tab())
                        tableau_duplique.set(i, indice_ligne_en_cours)
                        algo(tableau_duplique, indice_ligne_en_cours, nom + nom[-2:], nombre_de_resolus,
                             dernier_endroit_clique)

    else:  # si y'a plus de demandes
        # si on est à la dernière ligne
        if indice_ligne_en_cours == n - 1:
            # si la dernière ligne est pas ok, on s'arrête, sinon on affiche le tableau final
            demandes_sur_bordure_bas = tableau.compter_demandes_pour_ligne(n)
            if sum(demandes_sur_bordure_bas) != 0:
                # print("NON RESOLVABLE 1")
                return
            else:
                print("RESOLVAAaaaaaaaaaaaaaaaAAAAABLE")
                # tableau.print_tab()
                SOLUTIONS_TROUVEES.append(tableau)
                nombre_de_resolus += 1
                return
        else:
            # sinon, on passe à la ligne suivante
            algo(tableau, indice_ligne_en_cours + 1, nom[:-1] + str(indice_ligne_en_cours), nombre_de_resolus,
                 dernier_endroit_clique)
    # print("nombre_de_resolus = ", nombre_de_resolus)


# ici on va lancer l'algo sur les x possibilités générées par generate_sol_init()
solutions_init = generate_sol_init(n)
start = time.time()

for solution in solutions_init:
    solution = [1, 0, 0, 0, 0, 1]
    first_tableau = TABLEAU(n)
    for x in range(n):
        first_tableau.set(x, 0, solution[x])

    # on lance l'algo sur la solution
    algo(first_tableau, 1, "A1", 0, None)
    break
# break

# first_tableau = TABLEAU(n)
# first_tableau.set(1, 0)
# first_tableau.set(2, 0)
# first_tableau.set(3, 0)
# first_tableau.set(0, 1)
# first_tableau.set(1, 1)
# first_tableau.set(0, 2)
# first_tableau.set(2,2)
# first_tableau.set(0,3)
# # [[0. 1. 1. 1.]
# #  [1. 1. 0. 0.]
# #  [1. 0. 1. 0.]
# #  [0. 0. 0. 0.]]
# # algo(first_tableau,3,"A1")
# first_tableau.print_tab()
# print(first_tableau.compter_demandes_pour_ligne(4))

end = time.time()

# elimination des doublons
SOLUTIONS_UNIQUES = []
for sol in SOLUTIONS_TROUVEES:
    pas_dedans = True
    for sol2 in SOLUTIONS_UNIQUES:
        if (sol2 == sol.copy_tab()).all():
            pas_dedans = False
    if pas_dedans:
        SOLUTIONS_UNIQUES.append(sol.copy_tab())

print("###############################")
print("affichage des solutions :")
print("###############################")
for sol in SOLUTIONS_UNIQUES:
    print(sol[1:n + 1, 1:n + 1])

print(len(SOLUTIONS_UNIQUES), "solutions")
print("temps de calcul :", end - start)
