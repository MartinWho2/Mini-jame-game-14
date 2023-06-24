import pygame
from item import Item
from spritesheet import Spritesheet

class Animated_Item(Item):
	def __init__(self, window, type: str, original_position: pygame.Vector2, images_names: list[str], play_again: list[bool], grid, offset: pygame.Vector2, reverse_image: pygame.Surface):
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
		if self.type == 'player':
			self.powering = False
			self.powered_item = None
			self.powering_time = 0
			self.true_powering_time = 1000

	def dir_to_str(self, dir: pygame.Vector2):
		if dir == pygame.math.Vector2(0, -1):
			return "up"
		elif dir == pygame.math.Vector2(0, 1):
			return "down"
		elif dir == pygame.math.Vector2(-1, 0):
			return "left"
		elif dir == pygame.math.Vector2(1, 0):
			return "right"
	def tp_to_correct_tile(self):
		self.moving_time = self.true_moving_time
	def display(self, dt):
		if not self.reversing:
			image = self.spritesheets[self.active_spritesheet].update(dt)
			if image is None:
				if self.type == 'player':
					self.active_spritesheet = "Idle"
				elif self.type == 'guard':
					self.active_spritesheet = "gardien_idle_"+self.dir_to_str(self.direction)
				image = self.spritesheets[self.active_spritesheet].update(0)
			move_offset = pygame.Vector2(0,0)

			if self.moving:
				move_offset.x = self.direction.x * self.tile_size * (1 - self.moving_time / self.true_moving_time)
				move_offset.y = self.direction.y * self.tile_size * (1 - self.moving_time / self.true_moving_time)
			if self.type == 'player' or self.type == 'guard':
				if self.type == 'guard':
					for tile in self.visible_tiles:
						self.window.blit(self.yellow_surf,(tile[0] * self.tile_size + self.map_offset.x, tile[1] * self.tile_size + self.map_offset.y))
				elif self.type == 'player':
					if self.powering:
						if self.active_spritesheet == 'Idle':
							self.powering = False
							self.spritesheets[self.active_spritesheet].reset()
							self.active_spritesheet = "Idle"
							self.powered_item.reverse()

				self.window.blit(image, (self.position.x * self.tile_size + self.map_offset.x - move_offset.x,(self.position.y - 0.75) * self.tile_size + self.map_offset.y - move_offset.y))
			else:
				self.window.blit(image, (self.position.x * self.tile_size + self.map_offset.x - move_offset.x,
										 self.position.y * self.tile_size + self.map_offset.y - move_offset.y))
			if self.moving:
				self.moving_time += dt
				if self.moving_time > self.true_moving_time :
					self.moving = False
					self.moving_time = 0
					self.spritesheets[self.active_spritesheet].reset()
					if self.type == 'player':
						self.active_spritesheet = "Idle"
					elif self.type == 'guard':
						self.active_spritesheet = "gardien_idle_"+self.dir_to_str(self.direction)
					self.spritesheets[self.active_spritesheet].update(0)
		else:
			particles_image = self.particles_spritesheet.update(dt)

			move_offset = pygame.Vector2(0, 0)
			move_offset.x = self.direction.x * self.tile_size * self.moving_time / self.true_reversing_time
			move_offset.y = self.direction.y * self.tile_size * self.moving_time / self.true_reversing_time
			self.window.blit(self.reverse_image, (self.position.x * self.tile_size + self.map_offset.x + move_offset.x, (self.position.y-0.75) * self.tile_size + self.map_offset.y + move_offset.y))
			self.window.blit(particles_image, (self.position.x * self.tile_size + self.map_offset.x + move_offset.x, (self.position.y-0.75) * self.tile_size + self.map_offset.y + move_offset.y))
			self.window.blit(particles_image, (self.position.x * self.tile_size + self.map_offset.x + move_offset.x, self.position.y * self.tile_size + self.map_offset.y + move_offset.y))

			self.moving_time += dt
			if self.moving_time > self.true_reversing_time:
				self.movements.pop()
				if len(self.movements) == 0:
					self.position += self.direction
					if self.position == self.original_position:
						self.reversing = False
						self.direction = pygame.math.Vector2(0, 0)
						self.grid[int(self.original_position.y)][int(self.original_position.x)].enter(self)
						self.particles_spritesheet.update(0)
						if self.type == 'guard':
							self.find_visible_tiles()
					else:
						difference = self.position - self.original_position
						for i in range(int(abs(difference.x))):
							if difference.x>0:
								self.movements.append(pygame.math.Vector2(1 ,0))
							else:
								self.movements.append(pygame.math.Vector2(-1, 0))
						for j in range(int(abs(difference.y))):
							if difference.y > 0:
								self.movements.append(pygame.math.Vector2(0, 1))
							else:
								self.movements.append(pygame.math.Vector2(0, -1))
						self.direction = -self.movements[-1]
						self.particles_spritesheet.update(0)
				else:
					self.position += self.direction
					self.direction = -self.movements[-1]
					self.particles_spritesheet.update(0)
				self.moving_time = 0

	def reverse(self):
		if len(self.movements):
			self.direction = -self.movements[len(self.movements)-1]
			self.reversing = True
			self.active_tile.leave(self)
