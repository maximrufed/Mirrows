from game import *

class player():
	pos = geoma.point(0, 0)
	def __init__(self):
		self.pos.set(0, 0)
	def set(self, p: geoma.point):
		self.pos = p

class game():
	UNINIT = 0
	TURN = 1
	WIN = 2

	dx = 100
	dy = 100
	tek_map: map = map()
	players = []
	players_color = [pygame.Color("Brown"), pygame.Color("Magenta"), pygame.Color("White")]
	tek_player = 0
	state = UNINIT
	surface: pygame.Surface
	screen: pygame.display

	tek_pt: geoma.point

	def __init__(self, screen_init: pygame.display, sur: pygame.Surface):
		self.state = self.UNINIT
		self.screen = screen_init
		self.surface = sur

	def load_map(self):
		self.tek_map.load()

	def turn(self):
		self.state = self.TURN
		while (self.state != self.WIN or self.state != self.LOSE):
			if (self.state != self.TURN):
				break
			self.turn()
			# break

	def draw1(self):
		self.surface.fill(pygame.Color("WHITE"))
		self.tek_map.draw(self.surface, GREEN, RED, BLUE, 3, 3, 3)
		print(len(self.players))
		for i in range(len(self.players)):
			# print(self.players[i])
			pygame.draw.circle(self.surface, self.players_color[i], self.players[i].pos.to_arr(), 5)
		if (len(self.players) < 2):	pygame.draw.circle(self.surface, self.players_color[len(self.players)], self.tek_pt.to_arr(), 5)
		# if self.mode == 1 and self.sel_reb != []:
		# 	self.draw_sel_reb()
		# if self.mode == 1:
		# 	tek = pygame.mouse.get_pos()
		# 	num = self.find_nearest_reb(geoma.point(tek[0] - self.dx, tek[1] - self.dy))
		# 	self.draw_reb(num, self.sel_time_color)
		# if (self.mode == 1 and self.is_obl):
		# 	a = min(self.point1.x, self.point2.x)
		# 	b = min(self.point1.y, self.point2.y)
		# 	w = max(self.point1.x, self.point2.x) - a
		# 	h = max(self.point1.y, self.point2.y) - b
		# 	pygame.draw.rect(self.surface, self.rect_color, pygame.Rect(a, b, w, h))
		# if self.mode == 0 and self.is_first:
		# 	self.draw_new_reb()
		# if (self.mode == 0 and not(self.is_first)):
		# 	tek = pygame.mouse.get_pos()
		# 	pygame.draw.circle(self.surface, self.sel_time_color, self.get_point(geoma.point(tek[0], tek[1])).to_arr(), 5)
		self.screen.blit(self.surface, (self.dx, self.dy))
		pygame.display.update()

	def get_nearest(self, pt: geoma.point):
		dist = float("Inf")
		ans = -1
		for i in range(len(self.tek_map.start)):
			tek_dist = geoma.dist_pt_otr(pt, self.tek_map.start[i])
			if (dist - tek_dist >= geoma.eps):
				ans = i
				dist = tek_dist
		if (ans == -1):	return pt
		l = geoma.line(self.tek_map.start[ans].a, self.tek_map.start[ans].b)
		perp_line = geoma.perp_line_pt(l, pt)
		# return pt
		pt_inter = geoma.line_inter(perp_line, l)
		val = geoma.inside_pt_otr(pt, self.tek_map.start[ans])
		if (val == 0):
			return pt_inter
		elif (val == 1):
			return self.tek_map.start[ans].a
		elif (val == 2):
			return self.tek_map.start[ans].b

	def get_mouse_pos(self):
		a = pygame.mouse.get_pos()
		tek_pt = geoma.point(a[0] - self.dx, a[1] - self.dy)
		tek_pt = self.get_nearest(tek_pt)
		return tek_pt

	def get_point(self):
		run = True
		while run:
			self.tek_pt = self.get_nearest(self.get_mouse_pos())
			self.draw1()
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					exit()
				if event.type == pygame.KEYDOWN:
					if (event.key == pygame.K_ESCAPE):
						exit()
				if event.type == pygame.MOUSEBUTTONUP:
					return self.tek_pt

	def start_new_game(self):
		# load map
		self.load_map()

		# set start point for players
		self.players.clear()
		for i in range(2):
			a = player()
			a.set(self.get_point())
			self.players.append(a)
			self.draw1()

		# game_process
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					exit()
				if event.type == pygame.KEYDOWN:
					if (event.key == pygame.K_ESCAPE):
						exit()
		# end

	def start(self):
		self.start_new_game()

		# exit()
		# check for exit
		# while True:
		# 	for event in pygame.event.get():
		# 		if i.type == pygame.QUIT:
		# 			exit()
		# 		if event.type == pygame.KEYDOWN:
		# 			if (event.key == pygame.K_ESCAPE):
		# 				exit()


if __name__ == "__main__":
	pygame.init()
	screen = pygame.display.set_mode([1000, 1000])
	screen.fill(pygame.Color("lightgray"))
	pygame.display.update()

	tek_surf = pygame.Surface((800, 800))
	tek_game = game(screen, tek_surf)
	tek_game.start()
	pygame.quit()
