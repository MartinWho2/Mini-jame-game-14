import pygame
from item import Item
from spritesheet import Spritesheet

class Animated_Item(Item):
	def __init__(self, window, reverse : bool, original_position: pygame.Vector2, images_names: list[str], play_again: list[bool]):
		super().__init__(window, reverse, original_position)

		self.spritesheets = {}
		for i, animation in enumerate(images_names):
			spritesheet = Spritesheet(images_names[i], play_again[i], animation)
			self.spritesheets[images_names[i]] = spritesheet
		self.active_spritesheet = images_names[0]

	def display(self, dt):
		image = self.spritesheets[self.active_spritesheet].update(dt)
		if image is None:
			self.active_spritesheet = "monster"
			image = self.spritesheets[self.active_spritesheet].update(0)
		offset = pygame.Vector2(0,0)
		if self.moving:
			offset.x = self.direction.x * self.case_width * (1 - self.moving_time / self.true_moving_time)
			offset.y = self.direction.y * self.case_width * (1 - self.moving_time / self.true_moving_time)

		self.window.blit(image, (self.position.x * self.case_width + self.map_offset_x - offset.x ,
					self.position.y * self.case_width + self.map_offset_y - offset.y))
		if self.moving:
			self.moving_time += dt
			if self.moving_time > self.true_moving_time :
				self.moving = False
				self.moving_time = 0
				self.spritesheets[self.active_spritesheet].reset()
				self.active_spritesheet = "monster"
				self.spritesheets[self.active_spritesheet].update(0)