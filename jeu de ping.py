import numpy as np
import random, operator, copy,time
"""
l'ordre n'a pas d'importance
on arrive pas à résoudre un 3x3 ou 5x5 ou 7x7
en fait notre méthode de tri par ordre de score est peut-etre mauvaise
c'est pas parce qu'on a un bon score qu'on tend vers le tableau complet


bonjour je vais vous parler des nyctalope
	les nyctalopes ce ne sont pas des grosses putes comme on pourrait le penser
	en fait cest la capacité de voir dans le noir de certains animaux
	par exemple on peut dire que les chats sont des nyctalopes mais on peut aussi dire que ce sont des 

"""
n = 8
MAX = n*n

class CLIC():
	def __init__(self,clic_precedent):
		self.score = 0

		if clic_precedent==None:
			self.tableau = np.zeros((n,n))
		else:
			self.tableau = copy.deepcopy(clic_precedent.__tableau)

		self.position = (random.randint(0,n-1),random.randint(0,n-1))
		self.cliquer(self.position[0],self.position[1])

	def cliquer(self,x,y):
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
		self.sequence = [] #DEPRECATED tableau de clics
		self.positions_seq = [] #tableau des positions
		self.n_clics = clics
		self.generer()
		self.final_tableau_list = [] #DEPRECATED

	def mutate(self):
		cut_pos = random.randint(0,len(self.sequence))
		mutated_tab = self.sequence[:cut_pos]

		for i in range(0,self.n_clics - cut_pos):
			if i==0:
				clic = CLIC(self.sequence[cut_pos])
			else:
				clic = CLIC(last_clic)
			last_clic = clic
			mutated_tab.append(clic)

		self.final_tableau_list = mutated_tab

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
		self.n_solutions = 2000 #2000 -> 378s, 400 -> 837s
		self.mutation_percentage = 20/100
		# self.reproduction_percentage = 70/100
		self.selection_percentage = 30/100
		# self.separator = 50/100 #%

	def trier_solution(self):
		for solution in self.solutions:
			solution.evaluer()
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
		rep_sol = []
		for i in range(0,len(int(self.solutions/2)),2):
			rep_sol = self.solutions[i].final_tableau_list[:int(self.separator*len(self.final_tableau_list))] + self.solutions[i+1].final_tableau_list[int(self.separator*len(self.final_tableau_list)):]
			rep_sol.append(rep)
		self.solutions = rep_sol

	def generer(self):
		for i in range(self.n_solutions-len(self.solutions)):
			self.solutions.append(SOLUTION())


"""
TEST POUR CHAQUE NB DE CLICS
"""
scoremax=0
clics=50
# while clics>0:
# 	# print("recherche, clics : "+str(clics))
essais = 0

debut = time.time()
gen = GENERATION()

while scoremax!=MAX and essais<1000:
	gen.muter_solution()
	gen.trier_solution()
	gen.generer()
	# gen.reproduire_solution()

	scoremax=gen.solutions[0].score_max
	essais+=1
	print("essai n°",essais,"score :",scoremax, len(gen.solutions))

gen.solutions[0].suprEntreCommuns()
print("clics : ",len(gen.solutions[0].final_tableau_list),", score max : ",(gen.solutions[0].score_max==MAX)*" ",gen.solutions[0].score_max)
for tb in gen.solutions[0].final_tableau_list:
	print(tb)

# clics-=1
scoremax=0
print("temps total : ",time.time()-debut)