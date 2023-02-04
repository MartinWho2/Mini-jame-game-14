import pygame
from animated_item import Animated_Item
from spritesheet import Spritesheet

class Tower(Animated_Item):
	def __init__(self, window:pygame.Surface, position: pygame.Vector2, cells, offset: pygame.Vector2, direction: tuple[int, int], non_reversible_objects):
		super().__init__(window, 'tower', position, ['laser_idle_down', 'laser_idle_right', 'laser_idle_up', 'laser_idle_left', 'laser_shooting_down', 'laser_shooting_right', 'laser_shooting_up', 'laser_shooting_left'],
						 [True, True, True, True, True, True, True, True], cells, offset, None)
		self.cells = cells
		self.shooting = True
		self.directions = ['up', 'down', 'left', 'right']
		self.direction = direction
		self.position = position
		self.tuple_directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
		self.sprite_group = non_reversible_objects
		self.lasers = pygame.sprite.Group()
		self.walkable = False
		try:
			self.direction_text = self.directions[self.tuple_directions.index(direction)]
		except:
			raise ValueError(f'The inputted laser direction is {direction}, which is invalid.')

		if self.shooting:
			self.active_spritesheet = f'laser_shooting_{self.direction_text}'
			self.create_lasers()
			print(len(self.lasers))

	def change_state(self):
		self.shooting = not self.shooting

		if self.active_spritesheet == f'laser_idle_{self.direction_text}':
			self.active_spritesheet = f'laser_shooting_{self.direction_text}'
		else:
			self.active_spritesheet = f'laser_idle_{self.direction_text}'

	def create_lasers(self):
		new_coords = (int(self.position.x +self.direction[0]),int(self.position.y +self.direction[1]))
		walkable = self.cells[new_coords[0]][new_coords[1]].walkable
		empty_cell = self.cells[new_coords[0]][new_coords[1]].can_enter() == 1

		while walkable and empty_cell:
			self.lasers.add(Laser(self.window, self.direction, new_coords, self.cells, self.map_offset,self))
			new_coords = (new_coords[0]+self.direction[0], new_coords[1]+self.direction[1])

			walkable = self.cells[new_coords[0]][new_coords[1]].walkable
			empty_cell = self.cells[new_coords[0]][new_coords[1]].can_enter() == 1

	def shoot(self, dt):
		self.create_lasers()

	def display_lasers(self, dt):
		for laser in self.lasers:
			laser : Animated_Item
			laser.display(dt)

class Laser(Animated_Item):
	def __init__(self, window, direction: tuple[int, int], pos: pygame.Vector2, grid, offset, tower: Tower):
		super().__init__(window, 'laser', pygame.Vector2(pos[0], pos[1]),['laser'], [True], grid, offset, None)
		self.direction = direction
		self.tower = tower
		spriteSheet = self.spritesheets[self.active_spritesheet]

		if self.direction[0] == 0:
			if self.direction[0] == 1:
				spriteSheet.rotate_spritesheet(90)
			else:
				spriteSheet.rotate_spritesheet(-90)
		else:
			if self.direction[0] == -1:
				spriteSheet.rotate_spritesheet(180)