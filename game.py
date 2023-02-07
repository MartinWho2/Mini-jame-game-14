import os.path
import random
import json

import pygame

from exit_door import Exit_Door
from player import Player
from guard import Guard
from box import Box
from field import Field
from laser import Tower
from hole import Hole
from button import Button
from door import Door
from walls import Wall
from flag import Flag
from text_button import TextButton
from field import Tile
class Game:
	def __init__(self, window: pygame.surface.Surface, level_nb: int):
		# Levels
		self.levels_file = 'levels.json'
		self.levels = self.read_levels_file()

		self.guard_path_1 = self.get_guard_path(self.levels["1"]['guard'][0][2])


		self.menu = True
		self.menu_screen = 0
		self.window = window
		self.tile_size = 64
		self.level_nb = level_nb
		self.level_strings = ['1', '2','3','4','5','6','7','8']
		self.grid = []
		self.reversable_objects = pygame.sprite.Group()
		self.guards = pygame.sprite.Group()
		self.towers = pygame.sprite.Group()
		self.buttons = pygame.sprite.Group()
		self.non_reversible_objects = pygame.sprite.Group()
		self.time = pygame.time.get_ticks()
		self.dt = 0
		self.tile_image = pygame.image.load(os.path.join("Images","tiles.png"))
		self.MAP_SIZE = (10,10)
		self.field = Field(self.MAP_SIZE,self.tile_size)
		self.field.generate_map()
		self.map_offset = pygame.Vector2(0,0)

		# SFX
		self.button_click_sound = pygame.mixer.Sound('sounds/Button_click2.wav')
		self.menu_music = pygame.mixer.Sound('sounds/game_jam_menu.wav')
		self.sound_volume = 0.5
		self.menu_music.set_volume(self.sound_volume)
		self.game_music = pygame.mixer.Sound('sounds/game_jam.wav')
		self.game_music.set_volume(self.sound_volume)

		self.player = Player(self.window, pygame.math.Vector2(5, 5), self.field.cells, self.map_offset, self.towers)
		#path1 = self.get_guard_path('uuullllllllddddrrrrdruurrr')
		# self.guard1 = Guard(self.window, pygame.math.Vector2(9, 5), self.field.cells, self.map_offset,
		# 					self.guard_path_1, self.sfx_on)
		# self.box1 = Box(self.window, pygame.math.Vector2(7, 7), self.field.box_images,self.field.cells, self.map_offset)
		# self.box2 = Box(self.window, pygame.math.Vector2(8, 7),self.field.box_images,self.field.cells, self.map_offset)
		# self.hole = Hole(self.window, pygame.math.Vector2(5, 8),self.field.hole_images,self.field.cells, self.map_offset)
		# self.tower1 = Tower(self.window, True, pygame.math.Vector2(2, 2), self.field.cells, self.map_offset, (1, 0),self.towers)
		# self.towers.add(self.tower1)
		# self.door1 = Door(self.window, True, True, pygame.math.Vector2(4, 1), self.field.door_images, self.field.cells, self.map_offset)
		# self.button1 = Button(self.window, self.tower1, pygame.math.Vector2(2, 4),self.field.button_images, self.field.cells, self.map_offset)
		# self.button2 = Button(self.window, self.door1, pygame.math.Vector2(2, 6), self.field.button_images, self.field.cells, self.map_offset)
		# self.reversable_objects.add(self.guard1)
		# self.guards.add(self.guard1)
		# self.buttons.add(self.button1)
		# self.buttons.add(self.button2)
		# self.reversable_objects.add(self.box1)
		# self.reversable_objects.add(self.box2)
		# self.reversable_objects.add(self.player)
		#
		# self.non_reversible_objects.add(self.hole)
		# self.non_reversible_objects.add(self.door1)
		# self.non_reversible_objects.add(self.button1)
		# self.non_reversible_objects.add(self.button2)
		#
		# self.wall1 = Wall(self.window, 9, pygame.math.Vector2(9,9 ), self.field.walls_images, self.field.cells, self.map_offset)
		# self.non_reversible_objects.add(self.wall1)

		# Menu images
		self.size_map = 12 * self.tile_size
		self.main_menu_image = pygame.image.load(os.path.join("Images","menu_background.png"))
		self.main_menu_image = pygame.transform.scale(self.main_menu_image,(self.size_map,self.size_map))
		self.settings_image = pygame.image.load(os.path.join("Images","settings_background.png"))
		self.settings_image = pygame.transform.scale(self.settings_image,(self.size_map,self.size_map))
		self.level_select_image = pygame.image.load(os.path.join("Images","level_selection_background.png"))
		self.level_select_image = pygame.transform.scale(self.level_select_image, (self.size_map, self.size_map))
		# self.settings_text =  pygame.image.load(os.path.join("Images","settings.png"))
		# self.settings_text = pygame.transform.scale(self.settings_text, (self.settings_text.get_width()*4, self.settings_text.get_height()*4))
		# self.exit_text =  pygame.image.load(os.path.join("Images","exit.png"))
		# self.exit_text = pygame.transform.scale(self.exit_text, (self.exit_text.get_width()*4, self.exit_text.get_height()*4))
		# self.levels_text =  pygame.image.load(os.path.join("Images","levels.png"))
		# self.levels_text = pygame.transform.scale(self.levels_text, (self.levels_text.get_width()*4, self.levels_text.get_height()*4))
		# self.button_off_image = pygame.image.load(os.path.join("Images","button_off.png"))
		# self.button_off_image = pygame.transform.scale(self.button_off_image, (self.button_off_image.get_width()*4, self.button_off_image.get_height()*4))
		# self.button_on_image = pygame.image.load(os.path.join("Images","button_on.png"))
		# self.button_on_image = pygame.transform.scale(self.button_on_image, (self.button_on_image.get_width()*4, self.button_on_image.get_height()*4))
		self.levels_button = TextButton(pygame.Vector2(3,3),"levels")
		self.settings_button = TextButton(pygame.Vector2(2,7),"settings")
		self.exit_button = TextButton(pygame.Vector2(7,9),"exit")
		self.main_buttons = [self.levels_button,self.settings_button,self.exit_button]
		self.level_buttons = []
		positions = [(4,3),(6,3),(2,6),(4,6),(6,6),(4,9),(6,9),(8,9)]
		for i in range(1,9):
			pos = positions[i-1]
			self.level_buttons.append(TextButton(pygame.Vector2(pos[0],pos[1]),str(i)))
		self.on_button_1 = TextButton(pygame.Vector2(7,3),"button_on")
		self.off_button_1 = TextButton(pygame.Vector2(7,3),"button_off")
		self.on_button_2 = TextButton(pygame.Vector2(7,7),"button_on")
		self.off_button_2 = TextButton(pygame.Vector2(7,7),"button_off")

		self.reverse_text = pygame.image.load(os.path.join("Images","reverses.png")).convert_alpha()
		self.reverse_text = pygame.transform.scale(self.reverse_text, (self.reverse_text.get_width()*2, self.reverse_text.get_height()*2))

		self.music_on = True
		self.sfx_on = True
		self.levels = self.read_levels_file()
		self.actual_level = None
		self.reverse_font = pygame.font.SysFont('Arial',20)

		self.restart_button = TextButton(pygame.math.Vector2(12,0), "restart")

	def generate_level(self):
		self.field.cells =[[None for j in range(self.MAP_SIZE[0]+2)] for i in range(self.MAP_SIZE[1]+2)] # Empty 2d array
		self.field.generate_map()
		self.reversable_objects.empty()
		self.guards.empty()
		self.towers.empty()
		self.buttons.empty()
		self.non_reversible_objects = pygame.sprite.Group()
		if self.level_nb == 9:
			self.level_nb = 1
			self.menu = True
			self.menu_screen = 0
		self.actual_level = self.levels[self.level_strings[self.level_nb-1]]

		for coo in self.actual_level['flag']:
			flag = Flag(self.window, pygame.math.Vector2(coo[0],coo[1]), self.field.cells, self.map_offset)
			self.non_reversible_objects.add(flag)
		for coo in self.actual_level['walls']:
			wall = Wall(self.window, 9, pygame.math.Vector2(coo[0],coo[1]), self.field.walls_images, self.field.cells, self.map_offset)
			self.non_reversible_objects.add(wall)
		for coo in self.actual_level['box']:
			box = Box(self.window, pygame.math.Vector2(coo[0], coo[1]), self.field.box_images, self.field.cells, self.map_offset)
			self.reversable_objects.add(box)
		for coo in self.actual_level['guard']:
			print(self.get_guard_path(coo[2]))
			guard = Guard(self.window, pygame.math.Vector2(coo[0], coo[1]), self.field.cells, self.map_offset, self.get_guard_path(coo[2]))
			self.reversable_objects.add(guard)
			self.guards.add(guard)
		for coo in self.actual_level['door']:
			vertical = True
			if not coo[3]== 'vertical':
				vertical = False
			door = Door(self.window, True, vertical, pygame.math.Vector2(coo[0], coo[1]), self.field.door_images, self.field.cells, self.map_offset)
			self.non_reversible_objects.add(door)
			for button in self.actual_level['button']:
				if button[2]==coo[2]:
					button = Button(self.window, door, pygame.math.Vector2(button[0], button[1]), self.field.button_images, self.field.cells, self.map_offset)
					self.non_reversible_objects.add(button)
					self.buttons.add(button)
		for coo in self.actual_level['tower']:
			if coo[3] == 'up':
				direction = (0,-1)
			elif coo[3] == 'down':
				direction = (0,1)
			elif coo[3] == 'right':
				direction = (1, 0)
			else:
				direction = (-1, 0)
			tower = Tower(self.window, True, pygame.math.Vector2(coo[0], coo[1]), self.field.cells, self.map_offset, direction, self.towers)
			self.towers.add(tower)
			for button in self.actual_level['button']:
				if button[2]==coo[2]:
					button_sprite = Button(self.window, tower, pygame.math.Vector2(button[0], button[1]), self.field.button_images, self.field.cells, self.map_offset)
					self.non_reversible_objects.add(button_sprite)
					self.buttons.add(button_sprite)
		for coo in self.actual_level['hole']:
			hole = Hole(self.window, pygame.math.Vector2(coo[0], coo[1]), self.field.hole_images, self.field.cells, self.map_offset)
			self.non_reversible_objects.add(hole)
		coo = self.actual_level['exit']
		self.field.cells[coo[0]][coo[1]] = Exit_Door(self.field.exit_door,pygame.math.Vector2(coo[0]*self.tile_size, coo[1]*self.tile_size))
		self.field.cells[coo[1]][coo[0]] = Tile(self.field.walls_images[0],False,pygame.math.Vector2(coo[1]*self.tile_size, coo[0]*self.tile_size),False)
		coo = self.actual_level['spawn']
		self.player = Player(self.window, pygame.math.Vector2(coo[0], coo[1]), self.field.cells, self.map_offset,
							 self.towers)
		self.reversable_objects.add(self.player)

		for i in range(2):
			self.change_sfx_status()

	def read_levels_file(self):
		with open(self.levels_file,) as f:
			levels = json.load(f)

		return levels

	def restart(self):
		self.generate_level()

	def update(self):
		if self.player.winning:
			self.level_nb += 1
			print("iuevbuiydzrbvu8bhuogvbhuodhnboiuhvoiusrhoui")
			self.restart()
			self.player.winning = False
		rev_img = self.reverse_font.render(str(self.player.number_of_reverses), True, (0,0,0))
		self.dt = pygame.time.get_ticks() - self.time
		self.time = pygame.time.get_ticks()
		if not self.menu:
			self.field.update(self.dt, self.window)

			for item in self.non_reversible_objects:
				item.display(self.dt)
			for item in self.reversable_objects:
				item.display(self.dt)
			for tower in self.towers:
				tower.display(self.dt)
				tower.display_lasers(self.dt)
			self.window.blit(self.reverse_text,(12*self.tile_size,80))
			self.window.blit(rev_img,(12*self.tile_size+10+ self.reverse_text.get_width(), 80))
			mouse_pos = pygame.mouse.get_pos()
			if self.restart_button.rect.collidepoint(mouse_pos):
				self.restart_button.set_on()
			else:
				self.restart_button.set_off()
			self.window.blit(self.restart_button.image, self.restart_button.rect)
		else:
			self.menu_update()
		if self.player.active_tile.__class__ == Exit_Door:
			self.level_nb += 1
			self.restart()

	def menu_update(self):
		mouse_pos = pygame.mouse.get_pos()
		if self.menu_screen == 0:
			self.window.blit(self.main_menu_image,self.map_offset)
			for button in self.main_buttons:
				if button.rect.collidepoint(mouse_pos):
					button.set_on()
				else:
					button.set_off()
				self.window.blit(button.image,button.rect)
		elif self.menu_screen == 1:
			self.window.blit(self.settings_image,self.map_offset)
			if self.on_button_1.rect.collidepoint(mouse_pos):
				self.on_button_1.set_on()
				self.off_button_1.set_on()
			else:
				self.on_button_1.set_off()
				self.off_button_1.set_off()
			if self.on_button_2.rect.collidepoint(mouse_pos):
				self.on_button_2.set_on()
				self.off_button_2.set_on()
			else:
				self.on_button_2.set_off()
				self.off_button_2.set_off()
			if self.sfx_on:
				self.window.blit(self.on_button_1.image,self.on_button_1.rect)
			else:
				self.window.blit(self.off_button_1.image,self.off_button_1.rect)
			if self.music_on:
				self.window.blit(self.on_button_2.image,self.on_button_2.rect)
			else:
				self.window.blit(self.off_button_2.image,self.off_button_2.rect)
		elif self.menu_screen == 2:
			self.window.blit(self.level_select_image,self.map_offset)
			for button in self.level_buttons:
				if button.rect.collidepoint(mouse_pos):
					button.set_on()
				else:
					button.set_off()
				self.window.blit(button.image, button.rect)

	def get_guard_path(self, path: str) -> list[pygame.Vector2]:
		directions = list(path)
		direction_chars = ['u', 'd', 'l', 'r'] # Up, down, left, right
		direction_tuples = [(0, -1), (0, 1), (-1, 0), (1, 0)]
		output = []

		for direction in directions:
			tuple = direction_tuples[direction_chars.index(direction)]
			output.append(pygame.Vector2(tuple[0], tuple[1]))

		return output

	def change_sfx_status(self):
		self.sfx_on = not self.sfx_on

		for guard in self.guards:
			guard.surprise_sound.set_volume(self.sound_volume if self.sfx_on else 0)

		for button in self.buttons:
			button.hover_sound.set_volume(self.sound_volume if self.sfx_on else 0)

		for item in self.reversable_objects:
			if item.type == 'box':
				item.dragging_sound.set_volume(self.sound_volume if self.sfx_on else 0)

		self.player.death_sound.set_volume(self.sound_volume if self.sfx_on else 0)

		self.button_click_sound.set_volume(self.sound_volume if self.sfx_on else 0)
	
	def change_music_status(self):
		self.music_on = not self.music_on

		self.menu_music.set_volume(self.sound_volume if self.music_on else 0)
		self.game_music.set_volume(self.sound_volume if self.music_on else 0)
