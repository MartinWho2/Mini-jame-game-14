import pygame
from spritesheet import Spritesheet

class Item(pygame.sprite.Sprite):
	def __init__(self, window, original_position: pygame.Vector2, grid, offset: pygame.Vector2):
		super().__init__()
		self.window = window
		self.original_position = original_position
		self.position = self.original_position
		self.moving = False
		self.moving_time = 0
		self.true_moving_time = 250
		self.true_reversing_time = 150
		self.direction = pygame.math.Vector2(0, 0)
		self.reversed = False
		self.reversing = False
		self.movements = []
		self.tile_size = 64
		self.map_offset = offset
		self.grid = grid
		self.active_tile = self.grid[int(self.position.x)][int(self.position.y)]
		self.active_tile.enter(self)
		self.particles_spritesheet = Spritesheet('reverse_particle', True, True)


