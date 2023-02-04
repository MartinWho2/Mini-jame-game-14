import pygame
from game import Game

pygame.init()
pygame.display.init()
pygame.mixer.pre_init()

WIDTH, HEIGHT = 1000, 800

window = pygame.display.set_mode((WIDTH,HEIGHT))
playing = True
level = 1
game = Game(window, level)

while playing:
	window.fill("pink")
	game.update()
	for e in pygame.event.get():
		if e.type == pygame.QUIT:
			pygame.quit()
			playing = False
		if e.type == pygame.KEYDOWN:
			if not game.player.moving:
				if e.key == pygame.K_w:
					game.player.move(pygame.math.Vector2(0,-1))
				elif e.key == pygame.K_a:
					game.player.move(pygame.math.Vector2(-1,0))
				elif e.key == pygame.K_s:
					game.player.move(pygame.math.Vector2(0,1))
				elif e.key == pygame.K_d:
					game.player.move(pygame.math.Vector2(1,0))

		# Check collision with item
		if e.type == pygame.MOUSEBUTTONUP:
			mouse_pos = e.pos
			mouse_pos = (int(mouse_pos[0] / game.tile_size), int(mouse_pos[1] / game.tile_size))
			for item in game.field.cells[mouse_pos[1]][mouse_pos[0]].objects_on_it:
				item.reverse()


	pygame.display.flip()
