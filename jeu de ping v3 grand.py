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

class PLATEAU():
	def __init__(self):
		self.tableau = np.zeros((H+2,W+2))

	def jouer_sequence(self,positions_seq,verbose=None):
		cut_seq = []
		for position in positions_seq:
			self.cliquer(position[0],position[1])
			if verbose:
				print(self.tableau,position)
			cut_seq.append(position)
			if self.evaluer()==MAX:
				print(cut_seq)
				break
		return positions_seq #TODO

	def cliquer(self,x,y):
		for _x in range(x,x+3):
			for _y in range(y,y+3):
				try:
					self.tableau[_x,_y] = not self.tableau[_x,_y]
				except:
					print("D",(x,y))
		self.tableau[x+1,y+1]= not self.tableau[x+1,y+1]

	def evaluer(self):
		return np.sum(self.tableau[1:-1,1:-1])

	def count_bonus(self):
		bonus = 0
		for x in range(1,self.tableau.shape[1]-1):
			for y in range(1,self.tableau.shape[0]-1):
				if self.tableau[x,y]==1:
					bonus+=self.__detect_bonus(x,y)*0.1
		return bonus
	#oublier les bonus, et parcourir chaque clic d'une séqu pour trouver le bon moment

	def __detect_bonus(self,X,Y):
		nb_zeros=0
		for x in range(X-1,X+2):
			for y in range(Y-1,Y+2):
				if self.tableau[x,y]==0:
					nb_zeros+=1
		return nb_zeros


class SOLUTION():
	def __init__(self):
		self.score_max = 0
		self.bonus_score = 0
		self.positions_seq = []
		self.plateau = PLATEAU()
		self.completer()

	def completer(self):
		positions_possibles = list(set(combinations_with_replacement(list(range(n)) + list(range(n)), 2)))

		for i in range(clics-len(self.positions_seq)): #on ne joue pas 2 fois le même coup
			# est-ce qu'on clique partout ou est-ce qu'on choisit de pas cliquer des fois ?? -> oui on choisit si len(positions_possibles)>clics
			pos = positions_possibles.pop(random.randrange(len(positions_possibles)))
			self.positions_seq.append(pos)# todo remplacer for par while
			if len(positions_possibles)==0:
				break


	def evaluer(self):
		self.positions_seq = self.plateau.jouer_sequence(self.positions_seq)
		self.score_max = 0
		prev_size = len(self.positions_seq)
		i_max = None
		plateau_temp = PLATEAU()
		for i in range(len(self.positions_seq)):
			pos = self.positions_seq[i]
			plateau_temp.jouer_sequence([pos])
			score_temp = plateau_temp.evaluer()
			if score_temp>self.score_max:
				self.score_max=score_temp
				i_max = i
		self.positions_seq = self.positions_seq[:i_max+1]#ensuite générer de nouveaux clics
		self.completer()
		#print("prev :",prev_size,"new :",len(self.positions_seq))

	def evaluer_bonus(self):
		self.positions_seq = self.plateau.jouer_sequence(self.positions_seq)
		tableau = self.plateau.tableau
		self.score_max = self.plateau.evaluer()
		self.bonus_score = self.plateau.count_bonus()

	def evaluer_nb_impair(self):
		tableau_clics = np.chararray((n+2,n+2),unicode=True)
		tableau_clics[:] = '_'
		for pos in self.positions_seq:
			tableau_clics[pos[0]+1,pos[1]+1] = "#"

		tableau = np.zeros((n+2,n+2))

		for y in range(1,1+W):
			for x in range(1,1+H):
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
	def __init__(self): #todo est-ce qu'on tendrait pas trop vite vers un score haut ?
		#todo voir pour la quadruple symétrie
		self.solutions = []
		self.n_solutions = 1000
		self.mutation_percentage = MUT_INIT
		self.reproduction_percentage = 0/100 #todo pas de repro mieux ?
		self.selection_percentage = 30/100
		self.separator = 50/100 #%

	def trier_solution(self,eval_type):
		for solution in self.solutions:
			if eval_type=="normal":
				solution.evaluer()
			elif eval_type=="imp":
				solution.evaluer_nb_impair()
			elif eval_type=="bonus":
				solution.evaluer_bonus()

		self.solutions = sorted(self.solutions, key=lambda solution: solution.score_max+solution.bonus_score)
		self.solutions.reverse()

		self.solutions = self.solutions[:int(self.selection_percentage*self.n_solutions)]

	def muter_solution(self):
		mut_sol = []
		# for solution in self.solutions[:int(self.mutation_percentage*self.n_solutions)]:
		range_mut = int((self.mutation_percentage*len(self.solutions)))
		for i in range(range_mut):
			solution = random.choice(self.solutions)
			solution.mutate()
			mut_sol.append(solution)
		self.solutions += mut_sol

	def reproduire_solution(self):
		# ici on pourrait couper le premier au moment où il avait le plus de 1
		for i in range(0,int(len(self.solutions)*self.reproduction_percentage),2):
			sol1 = random.choice(self.solutions)
			sol2 = random.choice(self.solutions)
			sol1.positions_seq = sol1.positions_seq[:int(self.separator*len(sol1.positions_seq))]+ sol2.positions_seq[int(self.separator*len(sol2.positions_seq)):]
			self.solutions.append(sol1)

	def generer(self):
		for i in range(self.n_solutions-len(self.solutions)):
			self.solutions.append(SOLUTION())




MUT_INIT = 100/100
debut = time.time()
gen = GENERATION()
scoremax = 0
essais = 0
scoremax_gen = 0
scores_per_gen = []

n = 6 #-> donc n+2 de large/haut
H = n
W = n
MAX = n*n
BONUS_pt = 1
clics = 17


while scoremax!=MAX and essais<100:
	gen.muter_solution()
	gen.reproduire_solution()
	gen.trier_solution("normal") #normal
	gen.generer()
	if gen.mutation_percentage>0:
		gen.mutation_percentage-=1/100

	scoremax=gen.solutions[0].score_max
	bonus_score = gen.solutions[0].bonus_score
	if scoremax>scoremax_gen:
		scoremax_gen=scoremax
	essais+=1
	scores_per_gen.append(scoremax)
	print("essai n°",essais,"score :",scoremax, len(gen.solutions),"bonus :",bonus_score,"mut :",gen.mutation_percentage)


# gen.solutions[0].suprEntreCommuns()
print("clics : ",clics," score max : ",scoremax_gen)
if (gen.solutions[0].score_max==MAX):
	print(gen.solutions[0].plateau.__tableau)
	for pos in gen.solutions[0].positions_seq:
		print(pos)
	plateau = PLATEAU()
	plateau.jouer_sequence(gen.solutions[0].positions_seq,True)

print("temps total : ",time.time()-debut)

plt.plot(range(essais),scores_per_gen,'b')
plt.plot([0,essais-1],[MAX,MAX],'r--')
plt.ylabel('Score')
plt.xlabel('Generations')
plt.axis([0, essais-1, 0, MAX+2])
plt.show()
