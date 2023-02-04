import os.path
import random

import pygame
from player import Player
from guard import Guard
from box import Box
from field import Field
from laser import Tower

class Game:
	def __init__(self, window: pygame.surface.Surface, level_nb: int):
		self.window = window
		self.tile_size = 64
		self.level_nb = level_nb
		self.level_strings = ['level_1', 'level_2']
		self.grid = []
		self.reversable_objects = pygame.sprite.Group()
		self.non_reversible_objects = pygame.sprite.Group()
		self.time = pygame.time.get_ticks()
		self.dt = 0
		self.tile_image = pygame.image.load(os.path.join("Images","tiles.png"))
		self.MAP_SIZE = (10,10)
		self.field = Field(self.MAP_SIZE,self.tile_size)
		self.field.generate_map()
		self.map_offset = pygame.Vector2(0,0)

		self.player = Player(self.window, pygame.math.Vector2(5, 5),self.field.cells, self.map_offset)
		self.guard1 = Guard(self.window, pygame.math.Vector2(8, 9), self.field.cells, self.map_offset)
		self.box1 = Box(self.window, pygame.math.Vector2(7, 7), self.field.box_images,self.field.cells, self.map_offset)
		self.box2 = Box(self.window, pygame.math.Vector2(8, 7),self.field.box_images,self.field.cells, self.map_offset)
		self.reversable_objects.add(self.player)
		self.reversable_objects.add(self.guard1)
		self.reversable_objects.add(self.box1)
		self.reversable_objects.add(self.box2)
		self.tower1 = Tower(self.window, pygame.math.Vector2(2, 2), self.field.cells, self.map_offset, (0, 1), self.non_reversible_objects)
		self.non_reversible_objects.add(self.tower1)


	def generate_level(self):
		self.read_level_file(self.level_strings[self.level_nb-1])

	@staticmethod
	def read_level_file( file: str):
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

		for item in self.reversable_objects:
			item.display(self.dt)
		for item in self.non_reversible_objects:
			item.display(self.dt)