import pygame
from item import Item
from spritesheet import Spritesheet

class Animated_Item(Item):
	def __init__(self, window, original_position: pygame.Vector2, images_names: list[str], play_again: list[bool], grid, offset: pygame.Vector2, reverse_image: pygame.Surface):
		super().__init__(window, original_position,grid, offset)

		self.spritesheets = {}
		for i, animation in enumerate(images_names):
			spritesheet = Spritesheet(images_names[i], play_again[i], animation)
			self.spritesheets[images_names[i]] = spritesheet
		self.active_spritesheet = images_names[0]
		self.reverse_image = reverse_image
		self.reversable = (reverse_image is not None)
		self.type = type
		if self.type == 'guard':
			self.visible_tiles = []
			self.yellow_surf = pygame.surface.Surface((self.tile_size,self.tile_size),pygame.SRCALPHA)
			self.yellow_surf.fill((250,250,0,50))

	def display(self, dt):
		if not self.reversing:
			image = self.spritesheets[self.active_spritesheet].update(dt)
			if image is None:
				self.active_spritesheet = "Idle"
				image = self.spritesheets[self.active_spritesheet].update(0)
			move_offset = pygame.Vector2(0,0)
			if self.moving:
				move_offset.x = self.direction.x * self.case_width * (1 - self.moving_time / self.true_moving_time)
				move_offset.y = self.direction.y * self.case_width * (1 - self.moving_time / self.true_moving_time)

			self.window.blit(image, (self.position.x * self.case_width + self.map_offset.x - move_offset.x ,
									 (self.position.y-0.75) * self.case_width + self.map_offset.y - move_offset.y))
			if self.moving:
				self.moving_time += dt
				if self.moving_time > self.true_moving_time :
					self.moving = False
					self.moving_time = 0
					self.spritesheets[self.active_spritesheet].reset()
					self.active_spritesheet = "Idle"
					self.spritesheets[self.active_spritesheet].update(0)
		else:
			particles_image = self.particles_spritesheet.update(dt)

			move_offset = pygame.Vector2(0, 0)
			move_offset.x = self.direction.x * self.case_width * self.moving_time / self.true_reversing_time
			move_offset.y = self.direction.y * self.case_width * self.moving_time / self.true_reversing_time
			self.window.blit(self.reverse_image, (self.position.x * self.case_width + self.map_offset.x + move_offset.x, (self.position.y-0.75) * self.case_width + self.map_offset.y + move_offset.y))
			self.window.blit(particles_image, (self.position.x * self.case_width + self.map_offset.x + move_offset.x, (self.position.y-0.75) * self.case_width + self.map_offset.y + move_offset.y))
			self.window.blit(particles_image, (self.position.x * self.case_width + self.map_offset.x + move_offset.x, self.position.y * self.case_width + self.map_offset.y + move_offset.y))

			self.moving_time += dt
			if self.moving_time > self.true_reversing_time:
				self.movements.pop()
				if len(self.movements) == 0:
					self.position += self.direction
					self.reversing = False
					self.position = self.original_position
					self.direction = pygame.math.Vector2(0, 0)
					self.grid[int(self.original_position.x)][int(self.original_position.y)].enter(self)
					self.particles_spritesheet.update(0)
				else:
					self.position += self.direction
					self.direction = -self.movements[len(self.movements) - 1]
					self.particles_spritesheet.update(0)
				self.moving_time = 0

	def reverse(self):
		print("joueur")
		if len(self.movements):
			self.direction = -self.movements[len(self.movements)-1]
			self.reversing = True
			self.active_tile.leave(self)
