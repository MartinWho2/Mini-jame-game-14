import pygame
class Item(pygame.sprite.Sprite):
	def __init__(self, window, original_position: pygame.Vector2, grid):
		super().__init__()
		self.window = window
		self.original_position = original_position
		self.position = self.original_position
		self.moving = False
		self.moving_time = 0
		self.true_moving_time = 250
		self.direction = pygame.math.Vector2(0, 0)
		self.reversed = False
		self.movements = []
		self.case_width = 64
		self.map_offset_x = 0
		self.map_offset_y = 0
		self.grid = grid
		self.active_tile = self.grid[int(self.position.x)][int(self.position.y)]
		self.active_tile.enter(self)


