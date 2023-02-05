import pygame
from animated_item import Animated_Item

class Flag(Animated_Item):
	def __init__(self,window, original_position: pygame.Vector2, grid, offset: pygame.Vector2):
		super().__init__(window, "flag", original_position, ["flag"],[True],grid, offset, None)

	def remove_item(self):
		self.grid[int(self.position.x)][int(self.position.y)].leave(self)
		self.kill()
