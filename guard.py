import pygame
from animated_item import Animated_Item
pygame.mixer.init()

class Guard(Animated_Item):
	def __init__(self, window, original_position, grid, offset: pygame.Vector2, path: list[pygame.Vector2]):
		reverse_image = pygame.image.load('Images/Reverse_Idle.png')
		reverse_image = pygame.transform.scale(reverse_image,(reverse_image.get_width() * 4, reverse_image.get_height() * 4))
		super().__init__(window, 'guard', original_position, ['gardien_idle_down',"gardien_idle_up","gardien_idle_right","gardien_idle_left", 'LeGardienGauche', 'LeGardienDroite', 'LeGardienUp', 'LeGardienDown'], [True,True,True,True, False, False, False, False], grid, offset, reverse_image)
		self.alert = False
		self.path = path
		self.path_count = 0
		self.visible_tiles = []
		self.find_real_visible_tiles()
		self.light_image = pygame.rect.Rect(0,0,self.tile_size,self.tile_size)

		self.surprise_sound = pygame.mixer.Sound('sounds/Surprise.wav')

	def move(self):
		if not self.alert:
			self.path_count = self.path_count + 1
			if self.path_count > len(self.path)-1:
				self.path_count = 0
				self.movements = []
			self.direction = self.path[self.path_count]
			next_cell = self.grid[int((self.position + self.direction).y)][int((self.position + self.direction).x)].can_enter()
			if next_cell == 1:
				self.grid[int(self.position.y)][int(self.position.x)].leave(self)
				self.grid[int((self.position + self.direction).y)][int((self.position + self.direction).x)].enter(self)
				if self.direction == (-1, 0):
					self.active_spritesheet = "LeGardienGauche"
				elif self.direction == (1, 0):
					self.active_spritesheet = "LeGardienDroite"
				elif self.direction == (0, -1):
					self.active_spritesheet = "LeGardienUp"
				elif self.direction == (0, 1):
					self.active_spritesheet = "LeGardienDown"
				else:

					self.active_spritesheet = "gardien_idle_" + self.dir_to_str(self.direction)


				self.position += self.direction
				self.movements.append(self.direction)
				self.moving = True
			else:
				self.active_spritesheet = "gardien_idle_" + self.dir_to_str(self.direction)
				self.movements.append(self.direction)
			self.find_real_visible_tiles()
			if self.detect_player():
				return 1


	def detect_player(self):
		for tile in self.visible_tiles:
			if self.grid[tile[1]][tile[0]].can_enter()==3:
				if not self.alert:
					self.surprise_sound.play(0)
				return 1
		return 0

	def find_real_visible_tiles(self):
		self.visible_tiles.clear()
		directions = [(0,0),(0,1),(0,-1),(1,0),(1,-1),(1,1),(2,0),(2,-1),(2,-2),(2,1),(2,2)]
		accepted_tiles = {1,3,4,10}
		required_tiles = [[],[],[],[],[],[],[3],[3,4],[3,4],[3,5],[3,5]]
		directions_visible = []
		if self.direction.x == 1:
			pass
		elif self.direction.x == -1:
			directions = [(-x,y) for x,y in directions]
		elif self.direction.y == 1:
			directions = [(y,x) for x,y in directions]
		elif self.direction.y == -1:
			directions = [(y,-x) for x,y in directions]
		self.visible_tiles.append((int(self.position.x), int(self.position.y)))
		for index,destination in enumerate(directions):
			real_dest = (int(self.position.x + destination[0]), int(self.position.y + destination[1]))
			if self.grid[real_dest[1]][real_dest[0]].can_enter() in accepted_tiles:
				can_see = True
				for i in required_tiles[index]:
					if not directions[i] in directions_visible:
						can_see = False
						break
				if can_see:
					directions_visible.append(destination)
					self.visible_tiles.append(real_dest)
