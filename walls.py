import pygame
from normal_item import Normal_Item

class Wall(Normal_Item):
	def __init__(self, window, orientation: int,original_position:pygame.Vector2, images, grid, offset):
		self.orientation = orientation
		super().__init__(window, 'wall',False, original_position, images, grid, offset)
