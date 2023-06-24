import pygame
import sys
from game import Game

pygame.init()
pygame.display.init()
pygame.mixer.pre_init()

WIDTH, HEIGHT = 1000, 12*64

window = pygame.display.set_mode((WIDTH,HEIGHT))
playing = True
level = 1
game = Game(window, level)
if game.music_on:
	game.menu_music.play(-1)
while playing:
	window.fill("pink")

	game.update()
	for e in pygame.event.get():
		if e.type == pygame.QUIT:
			pygame.quit()
			playing = False
			sys.exit(0)
		if e.type == pygame.KEYDOWN:
			if not game.player.moving and not game.player.reversing and not game.player.powering and not game.menu:
				vec = None
				if e.key == pygame.K_w:
					vec = pygame.math.Vector2(0,-1)
				elif e.key == pygame.K_a:
					vec = pygame.math.Vector2(-1,0)
				elif e.key == pygame.K_s:
					vec = pygame.math.Vector2(0,1)
				elif e.key == pygame.K_d:
					vec = pygame.math.Vector2(1,0)
				if vec is not None:
					if game.player.move(vec):
						game.restart()
					for button in game.buttons:
						print("refresh")
						button.refresh()
					for guard in game.guards:
						if guard.move():
							game.spotted = 1
			if e.key == pygame.K_ESCAPE:
				game.menu_screen = 0
				if not game.menu:
					game.game_music.stop()
					game.menu_music.play(-1)
				game.menu = True
		# Check collision with item
		if e.type == pygame.MOUSEBUTTONUP:
			if not game.menu:
				mouse_pos = e.pos
				mouse_pos = (int((mouse_pos[0]-game.map_offset[0]) / game.tile_size), int((mouse_pos[1]-game.map_offset[1]) / game.tile_size))
				if game.restart_button.rect.collidepoint(e.pos):
					game.restart()
				if game.player.number_of_reverses>0:
					try:
						for item in game.field.cells[mouse_pos[1]][mouse_pos[0]].objects_on_it:
							if item.reversable:
								game.player.power(item)
								game.player.number_of_reverses -=1
								for button in game.buttons:
									button.refresh()
					except:
						print('Mouse position probably out of the map')
			else:
				if game.menu_screen == 0:
					if game.levels_button.rect.collidepoint(e.pos):
						game.menu_screen = 2
						game.button_click_sound.play(0)
					elif game.settings_button.rect.collidepoint(e.pos):
						game.menu_screen = 1
						game.button_click_sound.play(0)
					elif game.exit_button.rect.collidepoint(e.pos):
						game.button_click_sound.play(0)
						pygame.quit()
						playing = False
				elif game.menu_screen == 1:
					if game.on_button_1.rect.collidepoint(e.pos):
						game.button_click_sound.play(0)
						game.change_sfx_status()
					elif game.on_button_2.rect.collidepoint(e.pos):
						game.button_click_sound.play(0)
						game.change_music_status()
				elif game.menu_screen == 2:
					for i in range(8):
						if game.level_buttons[i].rect.collidepoint(e.pos):
							game.button_click_sound.play(0)
							game.level_nb = i+1
							game.generate_level()
							print("loaded level "+str(i+1))
							game.menu_music.stop()
							game.game_music.play(-1)
							game.menu = False


	pygame.display.flip()
