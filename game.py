import geoma
import pygame
import easygui
import math

WHITE = (255, 255, 255)
RED = (225, 0, 50)
GREEN = (0, 225, 0)
BLUE = (0, 0, 225)
BLACK = (0, 0, 0)

class map_editor():
	screen: pygame.display
	surface: pygame.Surface
	dx = 100
	dy = 100
	tek_map: map

	mode: int # режим (ребра или точки) точки - 0; ребра - 1
	sel_reb: int # номер ребра
	is_first: int
	first_point: geoma.point
	second_point: geoma.point # точки отрезка
	reb_type: chr

	sel_color: pygame.Color
	sel_width: int

	def __init__(self, screen_init: pygame.display, surface_init):
		self.surface = surface_init
		self.screen = screen_init
		self.tek_map = map()
		self.mode = 1
		self.sel_reb = 0
		self.sel_color = pygame.Color("brown")
		self.sel_width = 6
		self.is_first = 0
		self.reb_type = "w"

	def save(self):
		self.tek_map.save()

	def load(self):
		self.tek_map.load()

	def draw_sel_reb(self):
		print("draw_reb")	
		tek_otr: geoma.otr
		num = self.sel_reb
		if (num >= len(self.tek_map.walls)):
			num -= len(self.tek_map.walls)
			if (num >= len(self.tek_map.start)):
				num -= len(self.tek_map.start)
				tek_otr = self.tek_map.finish[num]
			else:
				tek_otr = self.tek_map.start[num]
		else:
			tek_otr = self.tek_map.walls[num]
		pygame.draw.line(self.surface, self.sel_color, tek_otr.a.to_arr(), tek_otr.b.to_arr(), self.sel_width)

	def draw_new_reb(self):
		col = pygame.Color("GREEN")
		if (self.reb_type == "w"):
			col = pygame.Color("GREEN")
		if (self.reb_type == "s"):
			col = pygame.Color("BLUE")
		if (self.reb_type == "f"):
			col = pygame.Color("RED")
		pygame.draw.line(self.surface, col, self.first_point.to_arr(), self.second_point.to_arr(), 6)

	def draw(self):
		self.surface.fill(pygame.Color("WHITE"))
		self.tek_map.draw(self.surface, GREEN, RED, BLUE, 3, 3, 3)
		if self.mode == 1 and self.sel_reb != -1:
			self.draw_sel_reb()
		if self.mode == 0 and self.is_first:
			self.draw_new_reb()
		self.screen.blit(self.surface, (self.dx, self.dy))
		pygame.display.update()

	def get_point(self, pt: geoma.point):
		pt.x -= self.dx
		pt.y -= self.dy
		return pt

	def add_reb(self):
		o = geoma.otr(self.first_point, self.second_point)
		if (self.reb_type == "w"):
			self.tek_map.add_wall(o)
		elif (self.reb_type == "s"):
			self.tek_map.add_start(o)
		elif (self.reb_type == "f"):
			self.tek_map.add_finish(o)

	def start(self):
		run = True
		change = True
		while run:
			if change:
				change = False
				self.draw()
				
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					run = False
				if (self.mode == 0):
					if event.type == pygame.MOUSEBUTTONDOWN:
						if (event.button == 1):
							self.is_first = 1
							self.first_point = geoma.point(event.pos[0], event.pos[1])
							self.first_point = self.get_point(self.first_point)
							self.second_point = geoma.point(event.pos[0], event.pos[1])
							self.second_point = self.get_point(self.second_point)
							change = 1

					if (event.type == pygame.MOUSEMOTION):
						if (self.is_first):
							self.second_point = geoma.point(event.pos[0], event.pos[1])
							self.second_point = self.get_point(self.second_point)
							change = 1

					if event.type == pygame.MOUSEBUTTONUP:
						if (event.button == 1):
							if (self.is_first):
								self.add_reb()
								change = 1
								self.is_first = 0

						# return {"pos":event.pos, "type":event.button}
				if event.type == pygame.KEYDOWN:
					if (event.key == pygame.K_ESCAPE):
						run = False
					if (event.key == pygame.K_0 and self.mode != 0):
						self.mode = 0
						self.is_first = 0
						change = True
					if (event.key == pygame.K_1 and self.mode != 1):
						self.mode = 1
						self.is_first = 0
						change = True



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
			self.walls.append(geoma.otr(geoma.point(float(tek[0]), float(tek[1])), geoma.point(float(tek[2]), float(tek[3]))))
			j += 1
		for i in range(int(lines[1])):
			tek = lines[j].split(" ")
			self.start.append(geoma.otr(geoma.point(float(tek[0]), float(tek[1])), geoma.point(float(tek[2]), float(tek[3]))))
			j += 1
		for i in range(int(lines[2])):
			tek = lines[j].split(" ")
			self.finish.append(geoma.otr(geoma.point(float(tek[0]), float(tek[1])), geoma.point(float(tek[2]), float(tek[3]))))
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

	def draw(self, sc, color_wall, color_start, color_finish, width_wall, width_start, width_finish):
		for e in self.walls:	pygame.draw.line(sc, color_wall, e.a.to_arr(), e.b.to_arr(), width_wall)
		for e in self.start:	pygame.draw.line(sc, color_start, e.a.to_arr(), e.b.to_arr(), width_start)
		for e in self.finish:	pygame.draw.line(sc, color_finish, e.a.to_arr(), e.b.to_arr(), width_finish)

	def clear(self):
		self.walls.clear()
		self.start.clear()
		self.finish.clear()

	def add_wall(self, o):
		self.walls.append(o)

	def add_start(self, o):
		self.start.append(o)

	def add_finish(self, o):
		self.finish.append(o)

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

	pygame.init()
	screen = pygame.display.set_mode([1000, 1000])
	screen.fill(pygame.Color("lightgray"))
	pygame.display.update()

	tek_surf = pygame.Surface((800, 800))
	m = map_editor(screen, tek_surf)
	m.load()
	m.start()
	pygame.quit()
	
