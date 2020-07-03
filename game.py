import geoma
import pygame
import easygui

class map_editor():
	screen: pygame.display
	def __init__(self):
		pass

	def save(self):
		pass

	def load(self):
		pass

class player():
	pos: geoma.point
	def __init__(self):
		pos.set(0, 0)

class map():
	# walls = [geoma.otr(geoma.point(0, 0), geoma.point(0, 100)), geoma.otr(geoma.point(79, 35), geoma.point(3245.45432, 100.77))]
	# start = [geoma.otr(geoma.point(0, 0), geoma.point(20, 20))]
	# finish = [geoma.otr(geoma.point(20, 20), geoma.point(40, 40))]
	walls = []
	start = []
	finish = []

	def __init__(self):
		pass

	def load(self):
		path = easygui.fileopenbox("Выберите карту", "", "Maps/*.mirmap", [["*.*", "All files"]])
		print(path)
		f = open(path, "r")
		lines = f.readlines()
		f.close()
		self.walls.clear()
		self.start.clear()
		self.finish.clear()
		j = 3;
		for i in range(int(lines[0])):
			tek = lines[j].split(" ")
			self.walls.append(geoma.otr(geoma.point(tek[0], tek[1]), geoma.point(tek[2], tek[3])))
			j += 1
		for i in range(int(lines[1])):
			tek = lines[j].split(" ")
			self.start.append(geoma.otr(geoma.point(tek[0], tek[1]), geoma.point(tek[2], tek[3])))
			j += 1
		for i in range(int(lines[2])):
			tek = lines[j].split(" ")
			self.finish.append(geoma.otr(geoma.point(tek[0], tek[1]), geoma.point(tek[2], tek[3])))
			j += 1
		

	def save(self):
		path = easygui.filesavebox("Save map", "", "Maps/*.mirmap")
		print(path)
		f = open(path, "w")
		print(len(self.walls), file = f)
		print(len(self.start), file = f)
		print(len(self.finish), file = f)
		for e in self.walls:	print(e.a.x, e.a.y, e.b.x, e.b.y, file = f, end = '')
		for e in self.start:	print(e.a.x, e.a.y, e.b.x, e.b.y, file = f, end = '')
		for e in self.finish:	print(e.a.x, e.a.y, e.b.x, e.b.y, file = f, end = '')
		f.close()

class game():
	UNINIT = 0
	TURN = 1
	WIN = 2
	LOSE = 3

	tek_map: map
	players = []
	tek_player = 0
	state = UNINIT
	
	def __init__(self):
		self.state = self.UNINIT

	def load_map(self):
		pass

	def turn(self):
		pass

	def start(self):
		while (self.state != self.WIN or self.state != self.LOSE):
			turn()
			break

if __name__ == "__main__":
	# g = game()
	# g.load_map()
	# g.start()
	m = map()
	m.load()
	m.save()