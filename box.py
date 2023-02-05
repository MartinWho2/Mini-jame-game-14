import pygame
from normal_item import Normal_Item

class Box(Normal_Item):
	def __init__(self, window, original_position, images, grid, offset: pygame.Vector2):
		super().__init__(window, 'box', True, original_position, images, grid, offset)
		self.on_laser = None # Laser on which the box is placed
		self.dragging_sound = pygame.mixer.Sound('sounds/Box_pushed.wav')

	def move(self, direction):
		self.direction = direction
		self.moving = True
		self.position += direction
		self.movements.append(direction)
		self.active_tile.leave(self)
		self.grid[int(self.position.x)][int(self.position.y)].enter(self)
