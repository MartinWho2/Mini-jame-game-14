import pygame
from normal_item import Normal_Item
class Door(Normal_Item):
	def __init__(self, window, state, vertical, original_position, images, grid, offset: pygame.Vector2):
		self.state = state #True = ouvert
		self.vertical = vertical
		super().__init__(window,"door",False,original_position,images, grid, offset)

	def change_state(self):
		self.state = not self.state
