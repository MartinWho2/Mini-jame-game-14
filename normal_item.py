import pygame
from item import Item
from spritesheet import Spritesheet

class Normal_Item(Item):
	def __init__(self, window, type: str,reverse : bool, original_position: pygame.Vector2, images: list[pygame.Surface], grid, offset:pygame.Vector2):
		super().__init__(window, original_position, grid, offset)
		self.type = type
		if self.type == 'box':
			self.image = images[0]
			self.reverse_image = images[1]
			self.fallen = False
		elif self.type == 'hole':
			self.image = images[0]
			self.filled_image = images[1]
			self.falling_spritesheet = Spritesheet('box_animation', False, True)
			self.filling_box = None
			self.falling = False
			self.filled = False
		elif self.type == 'door':
			self.image = images[0]
			self.open_image = images[1]
			if not self.vertical:
				self.image = pygame.transform.rotate(self.image, 90)
				self.open_image = pygame.transform.rotate(self.open_image, 90)
		elif self.type == 'button':
			self.pushed_image = images[0]
			self.image = images[1]
		elif self.type == 'wall':
			dict = [
				images[0],pygame.transform.rotate(images[0],90),
				pygame.transform.rotate(images[1],180), pygame.transform.rotate(images[1],90),images[1], pygame.transform.rotate(images[1],-90),
				pygame.transform.rotate(images[2], 180), pygame.transform.rotate(images[2],90), images[2], pygame.transform.rotate(images[2],-90)
			]
			self.image = dict[self.orientation]

		else:
			self.image = images[0]

		self.reversable = reverse


	def display(self, dt):
		if not self.reversing:
			if self.type == 'hole':
				if self.falling:
					if not self.filling_box.moving:
						self.filling_box.fallen = True
						image = self.falling_spritesheet.update(dt)
						if not image:
							self.falling = False
							self.filled = True
							self.window.blit(self.filled_image, (self.position.x * self.tile_size + self.map_offset.x,self.position.y * self.tile_size + self.map_offset.y))
						else:
							self.window.blit(image, (self.position.x * self.tile_size + self.map_offset.x, self.position.y * self.tile_size + self.map_offset.y))
					else:
						self.window.blit(self.image, (self.position.x * self.tile_size + self.map_offset.x, self.position.y * self.tile_size + self.map_offset.y))
				else:
					if self.filled:
						self.window.blit(self.filled_image, (self.position.x * self.tile_size + self.map_offset.x, self.position.y * self.tile_size + self.map_offset.y))
					else:
						self.window.blit(self.image, (self.position.x * self.tile_size + self.map_offset.x, self.position.y * self.tile_size + self.map_offset.y))
			elif self.type == 'button':

				if self.state:
					self.window.blit(self.pushed_image, (self.position.x * self.tile_size + self.map_offset.x, self.position.y * self.tile_size + self.map_offset.y))
				else:
					self.window.blit(self.image, (self.position.x * self.tile_size + self.map_offset.x, self.position.y * self.tile_size + self.map_offset.y))
			elif self.type == 'door':
				if self.state:
					self.window.blit(self.open_image, (self.position.x * self.tile_size + self.map_offset.x, self.position.y * self.tile_size + self.map_offset.y))
				else:
					self.window.blit(self.image, (self.position.x * self.tile_size + self.map_offset.x, self.position.y * self.tile_size + self.map_offset.y))
			else:
				if self.type == 'box' and self.fallen:
					pass
				else:
					move_offset = pygame.Vector2(0, 0)
					if self.moving:
						move_offset.x = self.direction.x * self.tile_size * (1-self.moving_time / self.true_moving_time)
						move_offset.y = self.direction.y * self.tile_size * (1-self.moving_time / self.true_moving_time)
					self.window.blit(self.image, (self.position.x * self.tile_size + self.map_offset.x - move_offset.x , self.position.y * self.tile_size + self.map_offset.y - move_offset.y))
					if self.moving:
						self.moving_time += dt
						if self.moving_time > self.true_moving_time :
							self.moving = False
							self.moving_time = 0
		else:
			particles_image = self.particles_spritesheet.update(dt)

			move_offset = pygame.Vector2(0, 0)
			move_offset.x = self.direction.x * self.tile_size * self.moving_time / self.true_reversing_time
			move_offset.y = self.direction.y * self.tile_size * self.moving_time / self.true_reversing_time
			self.window.blit(self.reverse_image, (self.position.x * self.tile_size + self.map_offset.x + move_offset.x, self.position.y * self.tile_size + self.map_offset.y + move_offset.y))
			self.window.blit(particles_image, (self.position.x * self.tile_size + self.map_offset.x + move_offset.x, self.position.y * self.tile_size + self.map_offset.y + move_offset.y))

			self.moving_time += dt
			if self.moving_time > self.true_reversing_time:
				self.movements.pop()
				if len(self.movements) == 0:
					self.position += self.direction
					self.reversing = False
					self.position = self.original_position
					self.direction = pygame.math.Vector2(0, 0)
					self.grid[int(self.original_position.y)][int(self.original_position.x)].enter(self)
					self.particles_spritesheet.update(0)
				else:
					self.position += self.direction
					self.direction = -self.movements[len(self.movements)-1]
					self.particles_spritesheet.update(0)
				self.moving_time = 0

	def reverse(self):
		if len(self.movements):
			self.direction = -self.movements[len(self.movements)-1]
			if self.type == 'box':
				if self.fallen:
					self.fallen = False
					hole = self.grid[int(self.position.y)][int(self.position.x)].get_hole()
					hole.filled = False
			self.reversing = True
			self.active_tile.leave(self)
