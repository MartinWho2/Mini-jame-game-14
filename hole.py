import pygame
from normal_item import Normal_Item

class Hole(Normal_Item):
	def __init__(self, window, original_position, images, grid, offset: pygame.Vector2):
		super().__init__(window, 'hole',False, original_position, images, grid, offset)

	def fall(self, box):
		self.falling = True
		self.filling_box = box




