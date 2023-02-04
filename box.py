import pygame
from normal_item import Normal_Item

class Box(Normal_Item):
	def __init__(self, window, original_position, images):
		super().__init__(window, True, original_position, images)
		self.type = 'box'

	def move(self, direction):
		self.direction = direction
		self.moving = True
		self.position += direction
		self.movements.append(direction)