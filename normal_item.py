import pygame
from item import Item

class Normal_Item(Item):
	def __init__(self, window, reverse : bool, original_position: pygame.Vector2, images: list[pygame.Surface]):
		super().__init__(window, reverse, original_position)
		if reverse:
			self.image = pygame.transform.scale(images[0], (4*images[0].get_width(), 4*images[0].get_height()))
			self.reverse_image = pygame.transform.scale(images[1], (4*images[1].get_width(), 4*images[1].get_height()))
		else:
			self.image = pygame.transform.scale(images[0], (4*images[0].get_width(), 4*images[0].get_height()))

	def display(self, dt):
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