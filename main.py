import geoma
import pygame

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

	# pt1 = geoma.point(100, 100)
	# pygame.draw.circle(screen, RED, pt1.to_arr(), 10)
	# pt1.rotate(0.5);
	# pygame.draw.circle(screen, RED, pt1.to_arr(), 10)

	# l = geoma.line(geoma.point(0, 0), geoma.point(0, 0))


	# mir = geoma.otr(get_point2(), get_point2())
	# ray = geoma.otr(get_point2(), get_point2())
	# mir = geoma.otr(geoma.point(100, 100), geoma.point(100, 200))
	# ray = geoma.otr(geoma.point(200, 50), geoma.point(150, 100))
	# draw_point(screen, mir.a, GREEN, 10)
	# draw_point(screen, mir.b, GREEN, 10)
	# draw_point(screen, ray.a, RED, 10)
	# draw_point(screen, ray.b, BLUE, 10)
	mir = geoma.otr(get_point2_draw(screen, GREEN, 1), get_point2_draw(screen, GREEN, 1))
	draw_line_otr(screen, mir, GREEN, 2)
	pygame.display.update()
	ray = geoma.otr(get_point2_draw(screen, RED, 2), get_point2_draw(screen, BLUE, 2))
	draw_line_otr(screen, ray, RED, 4)

	pygame.display.update()

	tek = geoma.inter_point(ray, mir)
	if (tek == -1):	
		print("No intersection")
	else:
		draw_line_otr(screen, tek, BLACK, 2)
		tek.a.show()
		tek.b.show()
		otraz = geoma.rotate_vector_vector(tek.to_vec(), mir.to_vec())
		draw_line(screen, tek.b, tek.b + otraz, BLACK, 2)


	pygame.display.update()

	# while 1:
		# tek_point = get_point()
		# pygame.draw.circle(screen, GREEN, tek_point["pos"], 20)
		# pygame.display.update()

	get_point()

	pygame.quit()

if __name__ == "__main__":
	start_game();