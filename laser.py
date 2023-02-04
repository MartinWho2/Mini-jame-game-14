import pygame
from animated_item import Animated_Item

class Tower(Animated_Item):
	def __init__(self, window, position, field, offset: pygame.Vector2, direction: tuple[int, int], non_reversible_objects):
		super().__init__(window, position, ['laser_idle', 'laser_shooting_down', 'laser_shooting_right'], [True, True, True], field, offset)
		self.field = field
		self.position = position
		self.type = 'laser'
		self.shooting = False
		self.directions = ['up', 'down', 'left', 'right']
		self.tuple_directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
		self.non_reversible_objects = non_reversible_objects
		try:
			self.direction = self.directions[self.tuple_directions.index(direction)]
		except:
			raise ValueError(f'The inputted laser direction is {direction}, which is invalid.')

	def change_state(self):
		self.shooting = not self.shooting

		if self.active_spritesheet == 'idle':
			self.active_spritesheet = f'shooting_{self.direction}'
		else:
			self.active_spritesheet = 'idle'

	def shoot(self):
		tile_coords = pygame.Vector2(int(self.position.x/self.field.tile_size), int(self.position.y/self.field.tile_size))

		tile_coords += pygame.Vector2(self.direction[0], self.direction[1])

		while self.field.cells[tile_coords.y][tile_coords.x].walkable and len(self.field.cells[tile_coords.y][tile_coords.x].objects_on_it) == 0:
			self.non_reversible_objects.add(Laser(self.window, self.direction, tile_coords))
			tile_coords[0] = tile_coords[0] + self.tuple_directions[0]
			tile_coords[1] = tile_coords[1] + self.tuple_directions[1]

class Laser(Animated_Item):
	def __init__(self, window, direction: tuple[int, int], pos: tuple[int, int]):
		super().__init__(window, pygame.Vector2(pos[0], pos[1]))
		self.direction = direction
		self.pos = pos

	def display(self):
		pass