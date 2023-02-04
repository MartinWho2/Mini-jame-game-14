import pygame
from normal_item import Normal_Item

class Box(Normal_Item):
	def __init__(self, window, original_position, images, grid):
		super().__init__(window, True, original_position, images, grid)
		self.type = 'box'

	def move(self, direction):
		self.direction = direction
		self.moving = True
		self.position += direction
		self.movements.append(direction)
		self.active_tile.leave(self)
		self.grid[int(self.position.x)][int(self.position.y)].enter(self)
