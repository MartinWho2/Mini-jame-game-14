import pygame
from spritesheet import Spritesheet

class Item(pygame.sprite.Sprite):
	def __init__(self, window, reverse : bool, original_position: pygame.Vector2):
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


	def reverse(self):
		pass

