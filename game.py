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
	sel_reb = [] # номер ребра
	is_first: int
	first_point: geoma.point
	second_point: geoma.point # точки отрезка
	reb_type: chr

	sel_color: pygame.Color
	sel_time_color: pygame.Color
	sel_width: int
	shift_pressed = 0

	def __init__(self, screen_init: pygame.display, surface_init):
		self.surface = surface_init
		self.screen = screen_init
		self.tek_map = map()
		self.mode = 1
		self.sel_reb = []
		self.sel_color = pygame.Color("lightblue")
		self.sel_time_color = pygame.Color("Brown")
		self.sel_width = 6
		self.is_first = 0
		self.reb_type = "w"
		self.is_obl = 0
		self.rect_color = pygame.Color("lightgray")
		self.point1 = geoma.point(0, 0)
		self.point2 = geoma.point(0, 0)
		self.last_point = geoma.point(0, 0)

	def clear(self):
		self.tek_map.clear()
		self.is_first = 0
		self.sel_reb = []

	def save(self):
		self.tek_map.save()

	def load(self):
		self.tek_map.load()
		self.is_first = 0
		self.sel_reb = []

	def draw_sel_reb(self):
		tek_otr: geoma.otr
		for num in self.sel_reb:
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
			col = pygame.Color("RED")
		if (self.reb_type == "f"):
			col = pygame.Color("BLUE")
		pygame.draw.line(self.surface, col, self.first_point.to_arr(), self.second_point.to_arr(), 6)

	def draw_reb(self, num: int, color: pygame.Color):
		if (num == -1): return
		if (num >= len(self.tek_map.walls)):
			num -= len(self.tek_map.walls)
			if (num >= len(self.tek_map.start)):
				num -= len(self.tek_map.start)
				self.first_point = self.tek_map.finish[num].a
				self.second_point = self.tek_map.finish[num].b
			else:
				self.first_point = self.tek_map.start[num].a
				self.second_point = self.tek_map.start[num].b
		else:		
			self.first_point = self.tek_map.walls[num].a
			self.second_point = self.tek_map.walls[num].b
		pygame.draw.line(self.surface, color, self.first_point.to_arr(), self.second_point.to_arr(), self.sel_width)

	def draw(self):
		self.surface.fill(pygame.Color("WHITE"))
		self.tek_map.draw(self.surface, GREEN, RED, BLUE, 3, 3, 3)
		if self.mode == 1 and self.sel_reb != []:
			self.draw_sel_reb()
		if self.mode == 1:
			tek = pygame.mouse.get_pos()
			num = self.find_nearest_reb(geoma.point(tek[0] - self.dx, tek[1] - self.dy))
			self.draw_reb(num, self.sel_time_color)
		if (self.mode == 1 and self.is_obl):
			a = min(self.point1.x, self.point2.x)
			b = min(self.point1.y, self.point2.y)
			w = max(self.point1.x, self.point2.x) - a
			h = max(self.point1.y, self.point2.y) - b
			pygame.draw.rect(self.surface, self.rect_color, pygame.Rect(a, b, w, h))
		if self.mode == 0 and self.is_first:
			self.draw_new_reb()
		if (self.mode == 0 and not(self.is_first)):
			tek = pygame.mouse.get_pos()
			pygame.draw.circle(self.surface, self.sel_time_color, self.get_point(geoma.point(tek[0], tek[1])).to_arr(), 5)
		self.screen.blit(self.surface, (self.dx, self.dy))
		pygame.display.update()

	def get_point(self, pt: geoma.point):
		pt.x -= self.dx
		pt.y -= self.dy
		ans = pt
		if (self.shift_pressed):
			dist = float("Inf")
			for x in self.tek_map.walls:
				tek_dist = (x.a - pt).len()
				if (dist - tek_dist > geoma.eps):
					ans = x.a
					dist = tek_dist
				tek_dist = (x.b - pt).len()
				if (dist - tek_dist > geoma.eps):
					ans = x.b
					dist = tek_dist
			for x in self.tek_map.start:
				tek_dist = (x.a - pt).len()
				if (dist - tek_dist > geoma.eps):
					ans = x.a
					dist = tek_dist
				tek_dist = (x.b - pt).len()
				if (dist - tek_dist > geoma.eps):
					ans = x.b
					dist = tek_dist
			for x in self.tek_map.finish:
				tek_dist = (x.a - pt).len()
				if (dist - tek_dist > geoma.eps):
					ans = x.a
					dist = tek_dist
				tek_dist = (x.b - pt).len()
				if (dist - tek_dist > geoma.eps):
					ans = x.b
					dist = tek_dist
			if (dist >= 50):
				ans = pt
		return ans

	def add_reb(self):
		o = geoma.otr(self.first_point, self.second_point)
		if (self.reb_type == "w"):
			self.tek_map.add_wall(o)
		elif (self.reb_type == "s"):
			self.tek_map.add_start(o)
		elif (self.reb_type == "f"):
			self.tek_map.add_finish(o)

	def add_sel_reb(self, num):
		for x in self.sel_reb:
			if (x == num): return
		self.sel_reb.append(num)

	def find_nearest_reb(self, pt: geoma.point):
		i = 0
		ans = -1
		dist = float("Inf")
		for j in range(len(self.tek_map.walls)):
			tek_dist = geoma.dist_pt_otr(pt, self.tek_map.walls[i])
			if (dist - tek_dist >= geoma.eps):
				ans = i
				dist = tek_dist
			i += 1
		tek = len(self.tek_map.walls)
		for j in range(len(self.tek_map.start)):
			tek_dist = geoma.dist_pt_otr(pt, self.tek_map.start[i - tek])
			if (dist - tek_dist >= geoma.eps):
				ans = i
				dist = tek_dist
			i += 1
		tek += len(self.tek_map.start)
		for j in range(len(self.tek_map.finish)):
			tek_dist = geoma.dist_pt_otr(pt, self.tek_map.finish[i - tek])
			if (dist - tek_dist >= geoma.eps):
				ans = i
				dist = tek_dist
			i += 1
		return ans

	def delete_reb(self):
		self.sel_reb.sort(reverse = True)
		for num in self.sel_reb:
			if (num >= len(self.tek_map.walls)):
				num -= len(self.tek_map.walls)
				if (num >= len(self.tek_map.start)):
					num -= len(self.tek_map.start)
					del self.tek_map.finish[num]
				else:
					del self.tek_map.start[num]
			else:
				del self.tek_map.walls[num]
		self.sel_reb = []

	def is_inside(self, p: geoma.point):
		if (min(self.point1.x, self.point2.x) <= p.x and p.x <= max(self.point1.x, self.point2.x)):
			if (min(self.point1.y, self.point2.y) <= p.y and p.y <= max(self.point1.y, self.point2.y)):
				return 1
		return 0

	def calc_walls(self):
		self.w1 = geoma.otr(geoma.point(self.point1.x, self.point1.y), geoma.point(self.point1.x, self.point2.y))
		self.w2 = geoma.otr(geoma.point(self.point2.x, self.point1.y), geoma.point(self.point2.x, self.point2.y))
		self.w3 = geoma.otr(geoma.point(self.point1.x, self.point1.y), geoma.point(self.point2.x, self.point1.y))
		self.w4 = geoma.otr(geoma.point(self.point1.x, self.point2.y), geoma.point(self.point2.x, self.point2.y))
		
	def check(self, o):
		if self.is_inside(o.a) or self.is_inside(o.b):
			return 1
		if (geoma.otr_inter(self.w1, o)):
			return 1
		if (geoma.otr_inter(self.w2, o)):
			return 1
		if (geoma.otr_inter(self.w3, o)):
			return 1
		if (geoma.otr_inter(self.w4, o)):
			return 1
		return 0

	def select_obl(self):
		self.calc_walls()
		i = 0
		for j in range(len(self.tek_map.walls)):
			if (self.check(self.tek_map.walls[j])):
				self.add_sel_reb(i)
			i += 1
		for j in range(len(self.tek_map.start)):
			if (self.check(self.tek_map.start[j])):
				self.add_sel_reb(i)
			i += 1
		for j in range(len(self.tek_map.finish)):
			if (self.check(self.tek_map.finish[j])):
				self.add_sel_reb(i)
			i += 1

	def start(self):
		run = True
		change = True
		while run:
			if change:
				# change = False
				self.draw()
				
			for event in pygame.event.get():
				pressed = pygame.key.get_pressed()

				self.shift_pressed = pressed[pygame.K_LSHIFT] or pressed[pygame.K_RSHIFT]

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
						if (event.button == 3):
							self.is_first = 1
							self.first_point = self.last_point
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
								self.last_point = geoma.point(event.pos[0] - self.dx, event.pos[1] - self.dy)
						if (event.button == 3):
							self.add_reb()
							change = 1
							self.is_first = 0
							self.last_point = self.second_point

				elif (self.mode == 1):
					if (event.type == pygame.MOUSEBUTTONDOWN):
						if (event.button == 1):
							tek = self.find_nearest_reb(geoma.point(event.pos[0] - self.dx, event.pos[1] - self.dy))
							for x in self.sel_reb:
								if (x == tek): tek = -1
							if (tek != -1):
								self.sel_reb.append(tek)
							change = 1

					if event.type == pygame.MOUSEBUTTONDOWN:
						if (event.button == 3):
							self.is_obl = 1
							self.point1 = geoma.point(event.pos[0], event.pos[1])
							self.point1 = self.get_point(self.point1)
							self.point2 = geoma.point(event.pos[0], event.pos[1])
							self.point2 = self.get_point(self.point2)
							change = 1

					if (event.type == pygame.MOUSEMOTION):
						if (self.is_obl):
							self.point2 = geoma.point(event.pos[0] - self.dx, event.pos[1] - self.dy)
							# self.point2 = self.get_point(self.point2)
						change = 1

					if event.type == pygame.MOUSEBUTTONUP:
						if (event.button == 3):
							if (self.is_obl):
								change = 1
								self.is_obl = 0
								self.select_obl()

				if event.type == pygame.KEYDOWN:
					if (event.key == pygame.K_ESCAPE):
						run = False
					
					if (event.key == pygame.K_0 and self.mode != 0):
						self.mode = 0
						self.is_first = 0
						self.is_obl = 0
						self.sel_reb = []
						change = True
					
					if (event.key == pygame.K_1 and self.mode != 1):
						self.mode = 1
						self.is_first = 0
						self.is_obl = 0
						self.sel_reb = []
						change = True

					if (event.key == pygame.K_s and (pressed[pygame.K_LCTRL] or pressed[pygame.K_RCTRL])):
						self.save()
						change = 1

					if (event.key == pygame.K_o and (pressed[pygame.K_LCTRL] or pressed[pygame.K_RCTRL])):
						self.load()
						change = 1

					if (event.key == pygame.K_n and (pressed[pygame.K_LCTRL] or pressed[pygame.K_RCTRL])):
						self.clear()
						change = 1

					# --------------

					if (event.key == pygame.K_w and self.reb_type != "w"):
						self.reb_type = "w"
						change = True

					if (event.key == pygame.K_s and self.reb_type != "s"):
						self.reb_type = "s"
						change = True

					if (event.key == pygame.K_f and self.reb_type != "f"):
						self.reb_type = "f"
						change = True

					if (event.key == pygame.K_DELETE and self.sel_reb != -1):
						self.delete_reb()
						change = 1



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
		f = open(path, "w")
		print(len(self.walls), file = f)
		print(len(self.start), file = f)
		print(len(self.finish), file = f)
		for e in self.walls:	print(e.a.x, e.a.y, e.b.x, e.b.y, file = f, end = '\n')
		for e in self.start:	print(e.a.x, e.a.y, e.b.x, e.b.y, file = f, end = '\n')
		for e in self.finish:	print(e.a.x, e.a.y, e.b.x, e.b.y, file = f, end = '\n')
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
	# m.load()
	m.start()
	pygame.quit()
	
