import numpy as np
import random, operator, copy,time,math
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
n = 6
H = n
W = n
MAX = n*n
clics = 16

class PLATEAU():
	def __init__(self):
		self.tableau = np.zeros((H,W))

	def jouer_sequence(self,positions_seq):
		for position in positions_seq:
			self.cliquer(position[0],position[1])

	def cliquer(self,x,y):
		if (x!=0 and y!=0): #en haut à gauche
			self.tableau[x-1,y-1]= not self.tableau[x-1,y-1]
		if (y!=0): #milieu haut
			self.tableau[x,y-1]= not self.tableau[x,y-1]
		if (x!=n-1 and y!=0): #haut droit
			self.tableau[x+1,y-1]= not self.tableau[x+1,y-1]
		if (x!=n-1): #gauche milieu
			self.tableau[x+1,y] = not self.tableau[x+1,y]
		if (x!=n-1 and y!=n-1): #bas droite
			self.tableau[x+1,y+1] = not self.tableau[x+1,y+1]
		if (y!=n-1): #milieu bas
			self.tableau[x,y+1] = not self.tableau[x,y+1]
		if (y!=n-1 and x!=0): #bas gauche
			self.tableau[x-1,y+1] = not self.tableau[x-1,y+1]
		if (x!=0): #milieu gauche
			self.tableau[x-1,y] = not self.tableau[x-1,y]		

	def evaluer(self):
		return np.sum(self.tableau)

	def count_bonus(self):
		for x in range(self.tableau.shape[1]):
			for y in range(self.tableau.shape[0]):




class SOLUTION():
	def __init__(self):
		self.score_max = 0
		self.positions_seq = []
		self.plateau = PLATEAU()

		positions_possibles = list(combinations_with_replacement(range(n),2))
		#print(positions_possibles)
		for i in range(clics): #on ne joue pas 2 fois le même coup
			pos = positions_possibles.pop()
			self.positions_seq.append(pos)
		#	print(pos)
			#print(random.randrange(math.pow(2,n)-i))

	def evaluer(self):
		self.plateau.jouer_sequence(self.positions_seq)
		self.score_max = self.plateau.evaluer()

	def evaluer_bonus(self):
		self.plateau.jouer_sequence(self.positions_seq)
		tableau = self.plateau.tableau
		self.score_max = self.plateau.evaluer() + self.plateau.count_bonus()




	def evaluer_nb_impair(self):
		tableau_clics = np.chararray((n,n),unicode=True)
		tableau_clics[:] = '_'
		for pos in self.positions_seq:
			tableau_clics[pos[0],pos[1]] = "#"

		tableau = np.zeros((n,n))

		for y in range(W):
			for x in range(H):
				if (x!=0 and y!=0): #en haut à gauche
					if tableau_clics[x-1,y-1]=="#":
						tableau[x,y]+=1
				if (y!=0): #milieu haut
					if tableau_clics[x,y-1] =="#":
						tableau[x,y]+=1
				if (x!=n-1 and y!=0): #haut droit
					if tableau_clics[x+1,y-1] =="#":
						tableau[x,y]+=1
				if (x!=n-1): #droite milieu
					if tableau_clics[x+1,y] =="#":
						tableau[x,y]+=1
				if (x!=n-1 and y!=n-1): #bas droite
					if tableau_clics[x+1,y+1] =="#":
						tableau[x,y]+=1
				if (y!=n-1): #milieu bas
					if tableau_clics[x,y+1] =="#":
						tableau[x,y]+=1
				if (y!=n-1 and x!=0): #bas gauche
					if tableau_clics[x-1,y+1]  =="#":
						tableau[x,y]+=1
				if (x!=0): #milieu gauche
					if tableau_clics[x-1,y] =="#":
						tableau[x,y]+=1

		# print(tableau)
		# print(tableau %2 == 1)
		# print(np.sum(tableau % 2 == 1))
		self.score_max = np.sum(tableau%2 == 1)

	def mutate(self):
		cut_pos = random.randint(0,len(self.positions_seq)-1)
		x = random.randint(0,n-1)
		y = random.randint(0,n-1)
		self.positions_seq[cut_pos] = ((x,y))

	def suprEntreCommuns(self):
		liste = []
		for position in self.positions_seq:
			liste.append(position)

		i = 0
		while i<len(liste):
			i_search= len(liste)-1
			while i_search > i:
				if liste[i] == liste[i_search]:
				# remove between
					for i_remove in range(i+1, i_search+1):
						liste[i_remove]=None
					break
				i_search-=1
			i+=1
		# self.sequence = list(filter(lambda a: a!=None,liste))

		new_list = []
		for i in liste:
			if i is not None:
				new_list.append(i)
		for i in range(len(new_list)):
			if new_list[i]==None:
				break
		self.final_tableau_list = new_list[:i]
		# self.sequence = list(filter(lambda a: not np.array_equal(a,np.zeros(n,n).fill(None)),liste))



class GENERATION():
	def __init__(self):
		self.solutions = []
		self.n_solutions = 500
		self.mutation_percentage = 20/100
		self.reproduction_percentage = 50/100
		self.selection_percentage = 20/100
		self.separator = 50/100 #%

	def trier_solution(self,eval_type):
		for solution in self.solutions:
			if eval_type=="normal":
				solution.evaluer()
			elif eval_type=="imp":
				solution.evaluer_nb_impair()
			elif eval_type=="bonus":
				solution.evaluer_bonus()
		self.solutions = sorted(self.solutions, key=lambda solution: solution.score_max)
		self.solutions.reverse()

		self.solutions = self.solutions[:int(self.selection_percentage*self.n_solutions)]

	def muter_solution(self):
		mut_sol = []
		for solution in self.solutions[:int(self.mutation_percentage*self.n_solutions)]:
			solution.mutate()
			mut_sol.append(solution)
		self.solutions += mut_sol

	def reproduire_solution(self):
		#ici on pourrait couper le premier au moment où il avait le plus de 1
		for i in range(0,int(len(self.solutions)/2),2):
			sol1 = self.solutions[i]
			sol2 = self.solutions[i+1]
			sol1.positions_seq = sol1.positions_seq[:int(self.separator*len(sol1.positions_seq))]+ sol2.positions_seq[int(self.separator*len(sol2.positions_seq)):]
			self.solutions.append(sol1)

	def generer(self):
		for i in range(self.n_solutions-len(self.solutions)):
			self.solutions.append(SOLUTION())



debut = time.time()
gen = GENERATION()
scoremax = 0
essais = 0
scoremax_gen = 0
scores_per_gen = []

while scoremax!=MAX and essais<100:
	gen.muter_solution()
	gen.reproduire_solution()
	gen.trier_solution("bonus") #normal
	gen.generer()
	# gen.reproduire_solution()

	scoremax=gen.solutions[0].score_max
	if scoremax>scoremax_gen:
		scoremax_gen=scoremax
	essais+=1
	scores_per_gen.append(scoremax)
	print("essai n°",essais,"score :",scoremax, len(gen.solutions))


# gen.solutions[0].suprEntreCommuns()
print("clics : "," score max : ",scoremax_gen)
# for pos in gen.solutions[0].positions_seq:
	# print(pos)
print("temps total : ",time.time()-debut)

plt.plot(range(essais),scores_per_gen,'b')
plt.plot([0,essais-1],[MAX,MAX],'r--')
plt.ylabel('Score')
plt.xlabel('Generations')
plt.axis([0, essais-1, 0, MAX+2])
plt.show()