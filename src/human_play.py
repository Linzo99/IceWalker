from grid import Grid
from random import choice
import os

grids = os.listdir("../datas/")
grid = choice(grids)

g = Grid.from_file(f"../datas/{grid}")

def repl_play(g):
	# variable pour verifier si le jeu est resolu
	resolved = False
	direction = ['N', 'S', 'E', 'O']
	while not resolved:
		print(g)
		entry = input("Entrez 'num,direction' pour faire mouvement : ou q(quit) ")
		if len(entry) == 1 and entry == 'q':
			print('Vous avez choisis de quitter le jeu')
			os.sys.exit()

		elif len(entry) == 3:

			try:
				mv, direc = entry.split(',')
				mv = int(mv)
				direc = direc.upper()
				assert direc in direction and mv in list(g.pers.keys())
			except AssertionError:
				print("Le mouvement ou joueur choisis n'est pas valide")
				continue
			except ValueError:
				print('Le numero du joueur est un nombre')
				continue
			except Exception as e:
				print(e)
				continue
		else:
			print("Entree non valide")
			continue

		resolved = move(mv, direc)
	print('Bravoooo vous avez gagne')
	print(g.__str__())



def move(mv, direc):	

		if direc == 'N':
			curpos = g.pers[mv]
			x, y = curpos
			if y > 0: 
				y-=1
				nextpos  = [y, x]
				while g.is_free(g.grid, nextpos):
					nextpos[0] -= 1
					continue
				
				g.clear_pos(curpos)
				g.update_pos((nextpos[0]+1, nextpos[1]), mv)
				return do_win((nextpos[1], nextpos[0]), mv)
			
		elif direc == 'S':
			curpos = g.pers[mv]
			x, y = curpos
			if y < 2*g.h: 
				y+=1
				nextpos  = [y, x]
				while g.is_free(g.grid, nextpos):
					nextpos[0] += 1
					continue
				
				g.clear_pos(curpos)
				g.update_pos((nextpos[0]-1, nextpos[1]), mv)
				return do_win((nextpos[1], nextpos[0]), mv)

		elif direc == 'O':
			curpos = g.pers[mv]
			x, y = curpos
			if x > 0: 
				x-=1
				nextpos  = [y, x]
				while g.is_free(g.grid, nextpos):
					nextpos[1] -= 1
					continue
				
				g.clear_pos(curpos)
				g.update_pos((nextpos[0], nextpos[1]+1), mv)
				return do_win((nextpos[1], nextpos[0]),mv)
			
			
		else :
			curpos = g.pers[mv]
			x, y = curpos
			if x < 2*g.w: 
				x+=1
				nextpos  = [y, x]
				while g.is_free(g.grid, nextpos):
					nextpos[1] += 1
					continue
				
				g.clear_pos(curpos)
				g.update_pos((nextpos[0], nextpos[1]-1), mv)
				return do_win((nextpos[1], nextpos[0]), mv)

def do_win(pos, mv):
	if pos == g.fCell and mv == 0:
		g.clear_pos(g.pers[0])
		g.clear_pos(g.fCell)
		g.update_pos((g.fCell[1], g.fCell[0]), 0)

		return True
	return False

repl_play(g)