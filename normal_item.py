import pygame
from item import Item

class Normal_Item(Item):
	def __init__(self, window, reverse : bool, original_position: pygame.Vector2, images: list[pygame.Surface], grid):
		super().__init__(window, original_position, grid)
		if reverse:
			self.image = images[0]
			self.reverse_image = images[1]
		else:
			self.image = images[0]

	def display(self, dt):
		if not self.reversing:
			offset = pygame.Vector2(0, 0)
			if self.moving:
				offset.x = self.direction.x * self.case_width * (1 - self.moving_time / self.true_moving_time)
				offset.y = self.direction.y * self.case_width * (1 - self.moving_time / self.true_moving_time)
			self.window.blit(self.image, (self.position.x * self.case_width + self.map_offset_x - offset.x , self.position.y * self.case_width + self.map_offset_y - offset.y))
			if self.moving:
				self.moving_time += dt
				if self.moving_time > self.true_moving_time :
					self.moving = False
					self.moving_time = 0
		else:
			offset = pygame.Vector2(0, 0)
			offset.x = self.direction.x * self.case_width * (1 - self.moving_time / self.true_reversing_time)
			offset.y = self.direction.y * self.case_width * (1 - self.moving_time / self.true_reversing_time)
			self.window.blit(self.reverse_image, (self.position.x * self.case_width + self.map_offset_x - offset.x,
										  self.position.y * self.case_width + self.map_offset_y - offset.y))
			self.moving_time += dt
			if self.moving_time > self.true_reversing_time:
				self.movements.pop()
				if len(self.:movements)movements
				self.reversing = False
				self.position += self.direction
				self.moving_time = 0

	def reverse(self):
		if len(self.movements):
			for movement in self.movements:
				self.direction = -movement
				self.reversing = True

			self.position = self.original_position
			self.direction = pygame.math.Vector2(0, 0)

