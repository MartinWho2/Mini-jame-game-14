import pygame
from item import Item

class Normal_Item(Item):
	def __init__(self, window, reverse : bool, original_position: pygame.Vector2, images: list[pygame.Surface], grid, offset:pygame.Vector2):
		super().__init__(window, original_position, grid, offset)
		if reverse:
			self.image = images[0]
			self.reverse_image = images[1]
		else:
			self.image = images[0]

	def display(self, dt):
		if not self.reversing:
			move_offset = pygame.Vector2(0, 0)
			if self.moving:
				move_offset.x = self.direction.x * self.case_width * (1-self.moving_time / self.true_moving_time)
				move_offset.y = self.direction.y * self.case_width * (1-self.moving_time / self.true_moving_time)
			self.window.blit(self.image, (self.position.x * self.case_width + self.map_offset.x - move_offset.x , self.position.y * self.case_width + self.map_offset.y - move_offset.y))
			if self.moving:
				self.moving_time += dt
				if self.moving_time > self.true_moving_time :
					self.moving = False
					self.moving_time = 0
		else:
			particles_image = self.particles_spritesheet.update(dt)

			move_offset = pygame.Vector2(0, 0)
			move_offset.x = self.direction.x * self.case_width * self.moving_time / self.true_reversing_time
			move_offset.y = self.direction.y * self.case_width * self.moving_time / self.true_reversing_time
			self.window.blit(self.reverse_image, (self.position.x * self.case_width + self.map_offset.x + move_offset.x, self.position.y * self.case_width + self.map_offset.y + move_offset.y))
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
					self.direction = -self.movements[len(self.movements)-1]
					self.particles_spritesheet.update(0)
				self.moving_time = 0

	def reverse(self):
		if len(self.movements):
			self.direction = -self.movements[len(self.movements)-1]
			self.reversing = True
			self.active_tile.leave(self)
