import pygame
from animated_item import Animated_Item
from spritesheet import Spritesheet

class Tower(Animated_Item):
	def __init__(self, window:pygame.Surface, state, position: pygame.Vector2, cells, offset: pygame.Vector2, direction: tuple[int, int], non_reversible_objects):
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
		self.first_laser = None
		self.num_lasers = 0
		self.state = state
		self.first_change = False

		try:
			self.direction_text = self.directions[self.tuple_directions.index(direction)]
		except:
			raise ValueError(f'The inputted laser direction is {direction}, which is invalid.')

		if self.shooting:
			self.active_spritesheet = f'laser_shooting_{self.direction_text}'
			self.create_lasers()
			print(len(self.lasers))
		self.update()

	def change_state(self):
		if self.first_change:
			self.state = not self.state
			self.shooting = not self.shooting

			if self.active_spritesheet == f'laser_idle_{self.direction_text}':
				self.active_spritesheet = f'laser_shooting_{self.direction_text}'
				self.create_lasers()
			else:
				self.active_spritesheet = f'laser_idle_{self.direction_text}'
				self.remove_all_lasers()
		else:
			self.first_change = True

	def update(self):
		if self.shooting:
			new_coords = (int(self.position.x +self.direction[0]), int(self.position.y +self.direction[1]))
			walkable = self.cells[new_coords[1]][new_coords[0]].walkable
			empty_cell = self.cells[new_coords[1]][new_coords[0]].get_box() is None
			empty_cell = empty_cell and (self.cells[new_coords[1]][new_coords[0]].get_wall() is None)
			number_of_free_tiles = 0

			while walkable and empty_cell:
				number_of_free_tiles += 1
				new_coords= (new_coords[1] + self.direction[1], new_coords[0] + self.direction[0])
				walkable = self.cells[new_coords[1]][new_coords[0]].walkable
				print(self.cells[new_coords[1]][new_coords[0]].can_enter())
				empty_cell = self.cells[new_coords[1]][new_coords[0]].get_box() is None

			if number_of_free_tiles != self.num_lasers:
				self.create_lasers()
				self.num_lasers = number_of_free_tiles

	def create_lasers(self):
		print("new fancy lasers")
		self.remove_all_lasers()
		print(f"There are {len(self.lasers)} lasers")
		new_coords = (int(self.position.y + self.direction[1]), int(self.position.x + self.direction[0]))
		walkable = self.cells[new_coords[1]][new_coords[0]].walkable
		empty_cell = self.cells[new_coords[1]][new_coords[0]].get_box() is None

		while walkable and empty_cell:
			laser = Laser(self.window,self.direction,pygame.Vector2(new_coords[0],new_coords[1]),self.grid,self.map_offset,self.lasers)
			self.lasers.add(laser)

			new_coords = (int(new_coords[0] + self.direction[0]), int(new_coords[1] + self.direction[1]))
			walkable = self.cells[new_coords[1]][new_coords[0]].walkable
			empty_cell = self.cells[new_coords[1]][new_coords[0]].get_box() is None and self.cells[new_coords[1]][new_coords[0]].can_enter() not in [0, 8]

	def remove_all_lasers(self):
		for laser in self.lasers:
			laser.get_out()

	def shoot(self, dt):
		self.create_lasers()

	def display_lasers(self, dt):
		for laser in self.lasers:
			laser : Animated_Item
			laser.display(dt)

class Laser(Animated_Item):
	def __init__(self, window, direction: tuple[int, int], pos: pygame.Vector2, grid, offset, sprite_group:pygame.sprite.Group):
		super().__init__(window, 'laser', pygame.Vector2(pos[0], pos[1]),['laser'], [True], grid, offset, None)
		self.direction = direction
		self.next_laser = None
		spriteSheet = self.spritesheets[self.active_spritesheet]
		self.sprite_group = sprite_group
		self.sprite_group.add(self)

		if self.direction[0] == 0:
			if self.direction[0] == 1:
				spriteSheet.rotate_spritesheet(90)
			else:
				spriteSheet.rotate_spritesheet(-90)
		else:
			if self.direction[0] == -1:
				spriteSheet.rotate_spritesheet(180)

	def create_next_lasers(self):
		new_pos = (int(self.position.x+self.direction[0]),int(self.position.y+self.direction[1]))
		print(new_pos, self.grid[new_pos[1]][new_pos[0]].can_enter(),self.grid[new_pos[1]][new_pos[0]].objects_on_it)
		if self.grid[new_pos[1]][new_pos[0]].can_enter() not in {0,2}:
			self.next_laser = Laser(self.window,self.direction,pygame.Vector2(int(new_pos[0]),int(new_pos[1])),self.grid,self.map_offset, self.sprite_group)
			self.next_laser.create_next_lasers()

	def create_laser(self):
		self.active_tile.enter(self)
		self.sprite_group.add(self)

	def get_out(self):
		self.active_tile.leave(self)
		self.kill()
