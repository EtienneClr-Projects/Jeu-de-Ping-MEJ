import time
import numpy as np, itertools

n = 4
H = n
W = n
MAX = n * n
clicsMax = 16


def generate_sol_init(n):
    combs = list(set(itertools.combinations_with_replacement([0, 1, 0, 1, 0, 1], n)))
    combs_no_duplicates = []
    combs_no_duplicates = combs
    # for i in range(len(combs)):
    #     combs[i] = list(combs[i])
    #
    # while len(combs) > 0:
    #     comb = combs.pop(0)
    #     if list(reversed(comb)) not in combs:
    #         combs_no_duplicates.append(comb)

    return combs_no_duplicates


# class Node():
#     def __init__(self, tableau, prev, nexts):
#         self.tableau = tableau
#         self.prev = prev
#         self.nexts = nexts
#
#
# class Tree():
#     def __init__(self):
#         self.initTree()
#
#     def initTree(self):
#         # pour un 4x4 on a 0000, 1000, 1100, 0100, 1110, 1111, 1010, 1001, 1011, 0110
#         firstCombs = generate_sol_init(n)
#
#         newNexts = []
#
#         self.firstElement = Node(None, )

class PLATEAU():
    def __init__(self):
        self.clicsTab = np.zeros((H + 2, W + 2))

    def jouer_sequence(self, positions_seq):
        for position in positions_seq:
            self.cliquer(position[0], position[1])

    def cliquer(self, x, y):
        x += 1
        y += 1
        self.clicsTab[x, y] = not self.clicsTab[x, y]

    def compter_clics_voisins_case(self, x, y):
        x += 1
        y += 1
        t = self.clicsTab
        return t[x - 1, y - 1] + t[x - 1, y] + t[x - 1, y + 1] + t[x, y + 1] + t[x, y - 1] + t[x + 1, y + 1] + t[
            x + 1, y] + t[x + 1, y - 1]

    def jouer(self):
        pass
        # self.cliquer(3, 3)
        # self.cliquer(3, 4)
        # print(self.compter_clics_voisins_case(4, 4))


def regarder_les_3_cases_au_dessus(x, y, t):
    # print("autour : " + str(regarder_cases_autour(x - 1, y - 1, t)),". coords : ",x,y)
    total = 0
    if x == 0 or x == n:
        return total
    if x > 1:
        total += verif_impair_cases_autour(x - 1, y - 1, t)
    total += verif_impair_cases_autour(x, y - 1, t)
    if x < n:
        total += verif_impair_cases_autour(x + 1, y - 1, t)
    return total


def verif_impair_cases_autour(x, y, t):
    # tt = (np.sum(t[y - 1:y + 2, x - 1:x + 2]) - t[y, x])
    # print("pour ", x, y, "\n", t[y - 1:y + 2, x - 1:x + 2], tt, "resultat :", (tt % 2 == 0) * 1)
    if 0 < x < n + 1:
        total = np.sum(t[y - 1:y + 2, x - 1:x + 2]) - t[y, x]
    elif x == 0:
        total = np.sum(t[y - 1:y + 2, x:x + 2] - t[y, x])
    elif x == n + 1:
        total = np.sum(t[y - 1:y + 2, x - 1:x + 1])
    # if (x > 0):
    #     total += t[y - 1, x - 1] + t[y, x - 1] + t[y + 1, x - 1]
    #     print(">0")
    # if (x < n + 1):
    #     print("<n")
    #     total += t[y - 1, x + 1] + t[y + 1, x + 1] + t[y, x + 1]
    # total += t[y - 1, x] + t[y + 1, x]
    # # print("tt",total,"xy",x,y)
    return (total % 2 == 0) * 1


# t = np.zeros((6, 6))
# # t[1, 2] = 1
# # t[2, 2] = 1
# print(regarder_les_3_cases_au_dessus(0, 2, t))
# t[2, 0] = 9
# print(t)
#
# quit()




def algo():
    nombre_de_resolus = 0
    for sol in sols_init:
        # initialisation du tableau
        print("#########################################################")
        print("test de la solution : " + str(sol))
        print("#########################################################")
        tableau_clics = np.zeros((n + 2, n + 2))  # +2 pour les bords
        for x in range(n):
            tableau_clics[1, x + 1] = sol[x]

        # on commence à la ligne 2 jusqu'en bas
        resolu_ou_non_resolvable = False
        for y in range(2, n + 1):
            ligne_au_dessus_est_rouge = False
            if resolu_ou_non_resolvable:
                break
            while not ligne_au_dessus_est_rouge:
                dernier_clic = -1
                print("\n\nWHIIIIIIIIIIIILE")
                # on regarde case par case si on clique dessus ou pas
                # pour savoir si on clique dessus :
                # on regarde les 3 cases au desssus
                # on compte le nombre de demandes pour cette case
                demandes_sur_cette_ligne = []
                for x in range(1, n + 1):  # initialisation de la ligne des demandes
                    demandes_sur_cette_ligne.append(regarder_les_3_cases_au_dessus(x, y, tableau_clics))
                    # if x == 3:
                    # print("DEBUUUG : ")
                    # print(regarder_les_3_cases_au_dessus(x, y, tableau_clics))
                    # print("DEBUUUG2: ", verif_impair_cases_autour(x+1, y - 1, tableau_clics))
                    # tableau_clics[y - 1, x] = 9

                # si y'a plus de demandes : la ligne est rouge on passe à la suivante
                if sum(demandes_sur_cette_ligne) == 0:
                    print("SUM=0")
                    # si on la ligne d'au dessus est rouge, mais que je suis à la dernière ligne
                    if y == n - 1:
                        # et que la dernière ligne est pas rouge --> non résolvable
                        # on regarde si la demande sur la bordure du bas est 0 pour chaque case
                        demandes_sur_bordure_bas = []
                        for i in range(1, n + 1):
                            demandes_sur_bordure_bas.append(regarder_les_3_cases_au_dessus(i, n - 1, tableau_clics))
                        if sum(demandes_sur_bordure_bas) != 0:
                            print("NON RESOLVABLE 1")
                        else:
                            print("RESOLVABLE")
                            nombre_de_resolus += 1
                            print(tableau_clics)
                        resolu_ou_non_resolvable = True
                    break

                else:  # si y'a encore des demandes
                    val_max = max(set(demandes_sur_cette_ligne))
                    # si y'a plusieurs fois le même nombre de demandes pour plusieurs cases, on prend la case la plus à gauche
                    if demandes_sur_cette_ligne.count(val_max) > 1:
                        # on clique sur la première case
                        # mais si on a déjà cliqué sur cette case, c'est que le tableau n'est pas résolvable
                        if tableau_clics[y, demandes_sur_cette_ligne.index(val_max) + 1] == 1:
                            print("NON RESOLVABLE 2")
                            resolu_ou_non_resolvable = True
                            break
                        else:
                            tableau_clics[y, demandes_sur_cette_ligne.index(val_max) + 1] = 1

                        print(">1" + str(demandes_sur_cette_ligne), "clic sur x=",
                              demandes_sur_cette_ligne.index(val_max) + 1, "y=", y)
                    else:  # si y'a qu'une seule demande max
                        # on clique sur la case avec la demande max
                        print("<=1")
                        tableau_clics[y, demandes_sur_cette_ligne.index(val_max) + 1] = 1
                print("ligne traitée=", y, "val=", val_max, "demande ind=", demandes_sur_cette_ligne.index(val_max),
                      demandes_sur_cette_ligne, "\nnouveau tab:\n", tableau_clics)
                # si la ligne d'au dessus n'est pas rouge, on recommence le comptage.
                # time.sleep(5)

sols_init = generate_sol_init(n)
nombre_de_resolus = 0
algo()


print("nombre_de_resolus = ", nombre_de_resolus, "/", len(sols_init))
