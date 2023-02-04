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
			if not game.player.moving and not game.player.reversing:
				if e.key == pygame.K_w:
					game.player.move(pygame.math.Vector2(0,-1))
					for guard in game.guards:
						guard.move()
				elif e.key == pygame.K_a:
					game.player.move(pygame.math.Vector2(-1,0))
					for guard in game.guards:
						guard.move()
				elif e.key == pygame.K_s:
					game.player.move(pygame.math.Vector2(0,1))
					for guard in game.guards:
						guard.move()
				elif e.key == pygame.K_d:
					game.player.move(pygame.math.Vector2(1,0))
					for guard in game.guards:
						guard.move()

		# Check collision with item
		if e.type == pygame.MOUSEBUTTONUP:
			mouse_pos = e.pos
			mouse_pos = (int((mouse_pos[0]-game.map_offset[0]) / game.tile_size), int((mouse_pos[1]-game.map_offset[1]) / game.tile_size))
			print(game.field.cells[mouse_pos[0]][mouse_pos[1]].objects_on_it)
			try:
				for item in game.field.cells[mouse_pos[0]][mouse_pos[1]].objects_on_it:
					if item.reversable:
						item.reverse()
			except:
				print('Mouse position probably out of the map')


	pygame.display.flip()
