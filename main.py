import geoma
import pygame
import game

WHITE = (255, 255, 255)
RED = (225, 0, 50)
GREEN = (0, 225, 0)
BLUE = (0, 0, 225)
BLACK = (0, 0, 0)

def get_point():
	run = True
	while run:
		for event in pygame.event.get():

			if event.type == pygame.QUIT:
				run = False

			if event.type == pygame.MOUSEBUTTONDOWN:
				return {"pos":event.pos, "type":event.button}

def get_point2():
	a = get_point()
	return geoma.point(a["pos"][0], a["pos"][1])

def get_point2_draw(sc, color, width):
	p = get_point2()
	draw_point(sc, p, color, width)
	pygame.display.update()
	return p

def get_key():
	run = True
	while run:
		for event in pygame.event.get():

			if (event.type == pygame.QUIT) or (event.type == pygame.KEYDOWN and event.key == 27):
				print("exit")
				run = False
				quit()
			
			if event.type == pygame.KEYDOWN:
				return event.key

def draw_point(sc, p, color, width):
	pygame.draw.circle(sc, color, p.to_arr(), width)

def draw_line(sc, p1, p2, color, width):
	pygame.draw.line(sc, color, p1.to_arr(), p2.to_arr(), width)

def draw_line_otr(sc, otr, color, width):
	pygame.draw.line(sc, color, otr.a.to_arr(), otr.b.to_arr(), width)

def draw_line(sc, p1, p2, color, width):
	pygame.draw.line(sc, color, p1.to_arr(), p2.to_arr(), width)

def start_game():
	pygame.init()
	screen = pygame.display.set_mode([1000, 1000])
	screen.fill(WHITE)
	pygame.display.update()

	map = game.map_editor(screen)
	map.draw()
	get_point()

	pygame.quit()

if __name__ == "__main__":
	start_game();