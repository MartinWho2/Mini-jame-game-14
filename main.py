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
					game.player.move(pygame.math.Vector2(0,-1), game.level_objects)
				elif e.key == pygame.K_a:
					game.player.move(pygame.math.Vector2(-1,0), game.level_objects)
				elif e.key == pygame.K_s:
					game.player.move(pygame.math.Vector2(0,1), game.level_objects)
				elif e.key == pygame.K_d:
					game.player.move(pygame.math.Vector2(1,0), game.level_objects)


	pygame.display.flip()
