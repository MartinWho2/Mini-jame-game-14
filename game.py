import os.path
import random

import pygame
from player import Player
from box import Box
from field import Field

class Game:
	def __init__(self, window: pygame.surface.Surface, level_nb: int):
		self.window = window
		self.tile_size = 64
		self.level_nb = level_nb
		self.level_strings = ['level_1', 'level_2']
		self.grid = []
		self.level_objects = pygame.sprite.Group()
		self.time = pygame.time.get_ticks()
		self.dt = 0
		self.tile_image = pygame.image.load(os.path.join("Images","tiles.png"))
		self.MAP_SIZE = (10,10)
		self.field = Field(self.MAP_SIZE,self.tile_size)
		self.field.generate_map()

		self.player = Player(self.window, pygame.math.Vector2(5, 5))
		self.box1 = Box(self.window, pygame.math.Vector2(7, 7), self.field.box_images)
		self.box2 = Box(self.window, pygame.math.Vector2(8, 7),self.field.box_images)
		self.level_objects.add(self.player)
		self.level_objects.add(self.box1)
		self.level_objects.add(self.box2)

	def generate_level(self):
		self.read_level_file(self.level_strings[self.level_nb-1])

	@staticmethod
	def read_level_file(self, file: str):
		with open(file, "r") as f:
			text = f.readline()
			f.close()
		## Create the map

	def restart(self):
		pass

	def update(self):
		self.dt = pygame.time.get_ticks() - self.time
		self.time = pygame.time.get_ticks()

		self.field.update(self.dt, self.window)

		for item in self.level_objects:
			item.display(self.dt)
