import pygame
from spritesheet import Spritesheet

class Item(pygame.sprite.Sprite):
	def __init__(self, window, original_position: pygame.Vector2, grid, offset: pygame.Vector2):
		super().__init__()
		self.window = window
		self.original_position = original_position
		self.position = pygame.math.Vector2(self.original_position.x, self.original_position.y)
		self.moving = False
		self.moving_time = 0
		self.true_moving_time = 250
		self.true_reversing_time = 100
		self.direction = pygame.math.Vector2(0, 0)
		self.reversed = False
		self.reversing = False
		self.active_tile = None
		self.movements = []
		self.tile_size = 64
		self.map_offset = offset
		self.grid = grid
		self.grid[int(self.position.y)][int(self.position.x)].enter(self)
		self.particles_spritesheet = Spritesheet('reverse_particle', True, True)
		self.type = ""


