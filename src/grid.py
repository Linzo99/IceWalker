class Grid:
	def __init__(self):
		Grid.w, Grid.h = (12,12) # w: width, h: height (largeur et longuer)
		Grid.fCell = (6, 7) #la case finale
		Grid.pos = [(1,1)] #position des personnages
		Grid.walls = ['3,6,E', '3,6,S'] #les murs
		Grid.cross = []
		#dictionnaire contenant la position des joueurs avec comme clef l'indice du personnage
		Grid.pers = dict()
		for key, value in enumerate(Grid.pos):
			Grid.pers[key] = value

		Grid.grid = Grid.init_build_grid()
	# permet de verifier si une case est libre 
	@staticmethod
	def is_free(grid, pos):
	
		return grid[pos[0]][pos[1]] == " "


	@staticmethod
	def update_pos(new, pers):
		Grid.grid[new[0]][new[1]] = str(pers)
		Grid.pers[pers] = (new[1],new[0])


	@staticmethod
	def clear_pos(pos):
		Grid.grid[pos[1]][pos[0]] = " "
	
	# permet d'avoir les intersections 
	def get_cross():
		cross = []
		for y in range(2, 2*Grid.h, 2):
			for x in range(2, 2*Grid.w, 2):
				count = 0
				if not Grid.is_free(Grid.result, (y,x-1)):
					count += 1
				if not Grid.is_free(Grid.result, (y,x+1)):
					count += 1
				if not Grid.is_free(Grid.result, (y+1,x)):
					count += 1
				if not Grid.is_free(Grid.result, (y-1,x)):
					count += 1
				if count > 1:
					cross.append((y,x))
		return cross

	@classmethod
	def from_file(cls, src):
		data = []
		with open(src, 'r') as file:
			lines = file.read().strip()

		lines = lines.split('\n')
		for line in lines:
			if not line.startswith('#'):
				data.append(line)

		cls.w, cls.h = map(int, data[0].split(',')) # w: width, h: height (largeur et longuer)
		cls.fCell = tuple(map(lambda x: 2*int(x)+1, data[1].split(','))) #la case finale
		cls.players = int(data[2]) # le nombre de personnage 
		cls.pos = [tuple(map(lambda x: 2*int(x)+1, ele.split(','))) for ele in data[3:(3+cls.players)]] #position des personnages
		cls.walls = data[(3+cls.players):] #les murs
		cls.cross = []
		#dictionnaire contenant la position des joueurs avec comme clef l'indice du personnage
		cls.pers = dict()
		for key, value in enumerate(cls.pos):
			cls.pers[key] = value

		cls.grid = cls.init_build_grid() # permet d'obtenir la grille finale
	
		return cls

	#permet de construire le rectangle initial
	@classmethod
	def init_build_grid(cls):
		cls.result = []
		for y in range(0, 2*(cls.h)+1):
			ligne = ''
			for x in range(0, 2*(cls.w)+1):
				if y == 0 or y == 2*(cls.h): # pour la première et dernière ligne
					ligne += '+' if not x%2 else '-' # + si la colonne est impair et - si c'est pair
				else:	# pour les autres lignes
					if y % 2 == 0 :	
						if x == 0 or x == 2*(cls.w):
							ligne+='+' 
						else:
							ligne += " "
					else:
						if x == 0 or x == 2*(cls.w):
							ligne+='|'
						else:
							ligne += " "
					
			# cls.result une liste contenant la liste des lignes ex: [['+','-','+',..],...]
			cls.result.append(list(ligne))

		# insertion de la position des joueurs
		for pos in cls.pos:
			cls.result[pos[1]][pos[0]] = str(cls.pos.index(pos))

		# insertion des murs
		for wall in cls.walls:
			wall = wall.split(',')
			x = 2*int(wall[0])+1
			y = 2*int(wall[1])+1
			if wall[-1] == 'E':
				x += 1
				cls.result[y][x] = '|'
			else:
				y += 1
				cls.result[y][x] = '-'

		# insertion des intersections
		cross = Grid.get_cross()
		for ele in cross:
			cls.result[ele[0]][ele[1]] = '+'
		# insertion de la case d'arrivee
		cls.result[cls.fCell[1]][cls.fCell[0]] = 'E'

		

		return cls.result

	@staticmethod
	def __str__():
		grille = ["".join(l) for l in Grid.grid]
		return "\n".join(grille)
		

		