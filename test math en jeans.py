import numpy as np
import random, operator, copy
"""
l'ordre n'a pas d'importance
on arrive pas à résoudre un 3x3 ou 5x5 ou 7x7

"""
n = 6
MAX = n*n

class CLIC():
	def __init__(self,clic_precedent):
		self.score = 0

		if clic_precedent==None:
			self.tableau = np.zeros((n,n))
		else:
			self.tableau = copy.deepcopy(clic_precedent.__tableau)

		self.position = (random.randint(0,n-1),random.randint(0,n-1))
		x=self.position[0]
		y=self.position[1]
		# print((x,y))
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


class SOLUTION():
	def __init__(self):
		self.score_max = 0
		self.i_score_max = 0
		self.sequence = [] #tableau de clics
		self.n_clics = clics
		self.generer()
		self.final_tableau_list = []

	def mutate(self):
		mutated = []
		for tab in self.final_tableau_list:
			mutated.append(numpy.invert(tab))
		self.final_tableau_list = mutated

	def evaluer(self):
		self.score_max = 0
		self.i_score_max = None
		for i in range(len(self.sequence)-1):
			score = self.sequence[i].evaluer()
			if score>self.score_max:
				self.score_max=score
				self.i_score_max = i
		return self.score_max

	def generer(self):
		self.sequence.append(CLIC(None))
		for i in range(1,self.n_clics):
			new_clic = CLIC(self.sequence[-1])
			self.sequence.append(new_clic)
			#print(new_clic.tableau)
		# print(self.sequence)

	def suprEntreCommuns(self):
		liste = []
		for i in self.sequence:
			liste.append(copy.deepcopy(i.__tableau))

		# i = 0
		# while i < len(liste):
		# 	# ind_end = list(reversed(liste)).index(liste[i])
		# 	ind_end = operator.indexOf(reversed(liste), liste[i])
		# 	liste = liste[:i] + liste[-ind_end - 1:]
		# 	i+=1

		i = 0
		while i<len(liste):
			i_search= len(liste)-1
			while i_search > i:
				if np.array_equal(liste[i],liste[i_search]):# liste[i] == liste[i_search]:
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
			if np.all(new_list[i],None):
				break
		self.final_tableau_list = new_list[:i+1]
		# self.sequence = list(filter(lambda a: not np.array_equal(a,np.zeros(n,n).fill(None)),liste))


class GENERATION():
	def __init__(self):
		self.solutions = []
		self.n_solutions = 1000
		self.mutation_percentage = 5/100
		self.reproduction_percentage = 15/100
		self.selection_percentage = 60/100
		self.separator = 50/100 #%

	def trier_solution(self):
		for solution in self.solutions:
			solution.evaluer()
		self.solutions = sorted(self.solutions, key=lambda solution: solution.score_max)
		self.solutions.reverse()

		self.solutions = self.solutions[:int(self.selection_percentage*self.n_solutions)]

	def muter_solution(self):
		mut_sol = []
		for solution in self.solutions[:int(self.mutation_percentage*len(self.solutions))]:
			mut_sol.append(solution.mutate())
		self.solutions = mut_sol

	def reproduire_solution(self):
		rep_sol = []
		for i in range(0,len(int(self.solutions/2)),2):
			rep_sol = self.solutions[i].final_tableau_list[:int(self.separator*len(self.final_tableau_list))] + self.solutions[i+1].final_tableau_list[int(self.separator*len(self.final_tableau_list)):]
			rep_sol.append(rep)
		self.solutions = rep_sol

	def generer(self):
		for i in range(self.n_solutions):
			self.solutions.append(SOLUTION())


"""
TEST POUR CHAQUE NB DE CLICS
"""
scoremax=0
clics=20
while clics>0:
	# print("recherche, clics : "+str(clics))
	essais = 0

	gen = GENERATION()
	while scoremax!=MAX and essais<50:
		gen.generer()
		gen.trier_solution()
		# gen.muter_solution()
		# gen.reproduire_solution()

		scoremax=gen.solutions[0].score_max
		essais+=1
		print(".",scoremax, len(gen.solutions))

	gen.solutions[0].suprEntreCommuns()
	print("clics : ",len(gen.solutions[0].final_tableau_list),", score max : ",(gen.solutions[0].score_max==MAX)*" ",gen.solutions[0].score_max)
	# for cl in gen.solutions[0].final_tableau_list:
	# 	print(cl)

	clics-=1
	scoremax=0