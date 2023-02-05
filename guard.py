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
		self.light_image = pygame.rect.Rect(0,0,self.tile_size,self.tile_size)

		self.surprise_sound = pygame.mixer.Sound('sounds/Surprise.wav')

	def move(self):
		if not self.alert:
			self.path_count = self.path_count + 1
			if self.path_count > len(self.path)-1:
				self.path_count = 0
				self.movements = []
			self.direction = self.path[self.path_count]
			next_cell = self.grid[int((self.position + self.direction).x)][int((self.position + self.direction).y)].can_enter()
			if next_cell == 1:
				self.grid[int(self.position.x)][int(self.position.y)].leave(self)
				self.grid[int((self.position + self.direction).x)][int((self.position + self.direction).y)].enter(self)
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
			self.visible_tiles.clear()
			self.find_visible_tiles()
			self.detect_player()


	def detect_player(self):
		for tile in self.visible_tiles:
			if self.grid[tile[0]][tile[1]].can_enter()==3:
				print("joueur détecté")


	def find_visible_tiles(self):
		## NE PAS EFFACER, JE SAIS QUE C'EST DEGUEULASSE MAIS J'AI PAS LE TEMPS DE TROUVER PLUS SIMPLE, AU PIRE REECRIVEZ A COTE
		self.visible_tiles.clear()
		self.visible_tiles.append((int(self.position.x),int(self.position.y)))
		if self.direction.y == 1 or self.direction == (0, 0):
			if self.grid[int(self.position.x+1)][int(self.position.y)].can_enter() in {1,3}:
				self.visible_tiles.append((int(self.position.x+1),int(self.position.y)))
				if self.grid[int(self.position.x + 1)][int(self.position.y+1)].can_enter() in {1,3}:
					self.visible_tiles.append((int(self.position.x + 1), int(self.position.y+1)))
					if self.grid[int(self.position.x + 1)][int(self.position.y + 2)].can_enter() in {1,3}:
						self.visible_tiles.append((int(self.position.x + 1), int(self.position.y + 2)))
					if self.grid[int(self.position.x + 2)][int(self.position.y + 2)].can_enter() in {1,3}:
						self.visible_tiles.append((int(self.position.x + 2), int(self.position.y + 2)))
			if self.grid[int(self.position.x-1)][int(self.position.y)].can_enter() in {1,3}:
				self.visible_tiles.append((int(self.position.x - 1), int(self.position.y)))
				if self.grid[int(self.position.x -1)][int(self.position.y+1)].can_enter() in {1,3}:
					self.visible_tiles.append((int(self.position.x -1), int(self.position.y+1)))
					if self.grid[int(self.position.x - 1)][int(self.position.y + 2)].can_enter() in {1,3}:
						self.visible_tiles.append((int(self.position.x - 1), int(self.position.y + 2)))
					if self.grid[int(self.position.x - 2)][int(self.position.y + 2)].can_enter() in {1,3}:
						self.visible_tiles.append((int(self.position.x - 2), int(self.position.y + 2)))
			if self.grid[int(self.position.x)][int(self.position.y+1)].can_enter() in {1,3}:
				self.visible_tiles.append((int(self.position.x), int(self.position.y+1)))
				if self.grid[int(self.position.x)][int(self.position.y+2)].can_enter() in {1,3}:
					self.visible_tiles.append((int(self.position.x),int(self.position.y + 2)))
		if self.direction.y == -1:
			if self.grid[int(self.position.x+1)][int(self.position.y)].can_enter() in {1,3}:
				self.visible_tiles.append((int(self.position.x+1),int(self.position.y)))
				if self.grid[int(self.position.x + 1)][int(self.position.y-1)].can_enter() in {1,3}:
					self.visible_tiles.append((int(self.position.x + 1), int(self.position.y-1)))
					if self.grid[int(self.position.x + 1)][int(self.position.y - 2)].can_enter() in {1,3}:
						self.visible_tiles.append((int(self.position.x + 1), int(self.position.y - 2)))
					if self.grid[int(self.position.x + 2)][int(self.position.y - 2)].can_enter() in {1,3}:
						self.visible_tiles.append((int(self.position.x + 2), int(self.position.y - 2)))
			if self.grid[int(self.position.x-1)][int(self.position.y)].can_enter() in {1,3}:
				self.visible_tiles.append((int(self.position.x - 1), int(self.position.y)))
				if self.grid[int(self.position.x -1)][int(self.position.y-1)].can_enter() in {1,3}:
					self.visible_tiles.append((int(self.position.x -1), int(self.position.y-1)))
					if self.grid[int(self.position.x - 1)][int(self.position.y - 2)].can_enter() in {1,3}:
						self.visible_tiles.append((int(self.position.x - 1), int(self.position.y - 2)))
					if self.grid[int(self.position.x - 2)][int(self.position.y - 2)].can_enter() in {1,3}:
						self.visible_tiles.append((int(self.position.x - 2), int(self.position.y - 2)))
			if self.grid[int(self.position.x)][int(self.position.y-1)].can_enter() in {1,3}:
				self.visible_tiles.append((int(self.position.x), int(self.position.y-1)))
				if self.grid[int(self.position.x)][int(self.position.y-2)].can_enter() in {1,3}:
					self.visible_tiles.append((int(self.position.x),int(self.position.y - 2)))
		if self.direction.x == 1:
			if self.grid[int(self.position.x)][int(self.position.y+1)].can_enter() in {1,3}:
				self.visible_tiles.append((int(self.position.x),int(self.position.y+1)))
				if self.grid[int(self.position.x + 1)][int(self.position.y+1)].can_enter() in {1,3}:
					self.visible_tiles.append((int(self.position.x + 1), int(self.position.y+1)))
					if self.grid[int(self.position.x + 2)][int(self.position.y + 1)].can_enter() in {1,3}:
						self.visible_tiles.append((int(self.position.x + 2), int(self.position.y + 1)))
					if self.grid[int(self.position.x + 2)][int(self.position.y + 2)].can_enter() in {1,3}:
						self.visible_tiles.append((int(self.position.x + 2), int(self.position.y + 2)))
			if self.grid[int(self.position.x)][int(self.position.y-1)].can_enter() in {1,3}:
				self.visible_tiles.append((int(self.position.x), int(self.position.y-1)))
				if self.grid[int(self.position.x +1)][int(self.position.y-1)].can_enter() in {1,3}:
					self.visible_tiles.append((int(self.position.x +1), int(self.position.y-1)))
					if self.grid[int(self.position.x +2)][int(self.position.y + 2)].can_enter() in {1,3}:
						self.visible_tiles.append((int(self.position.x + 2), int(self.position.y -1)))
					if self.grid[int(self.position.x + 2)][int(self.position.y - 2)].can_enter() in {1,3}:
						self.visible_tiles.append((int(self.position.x + 2), int(self.position.y - 2)))
			if self.grid[int(self.position.x+1)][int(self.position.y)].can_enter() in {1,3}:
				self.visible_tiles.append((int(self.position.x+1), int(self.position.y)))
				if self.grid[int(self.position.x+2)][int(self.position.y)].can_enter() in {1,3}:
					self.visible_tiles.append((int(self.position.x+2),int(self.position.y)))
		if self.direction.x == -1:
			if self.grid[int(self.position.x)][int(self.position.y+1)].can_enter() in {1,3}:
				self.visible_tiles.append((int(self.position.x),int(self.position.y+1)))
				if self.grid[int(self.position.x - 1)][int(self.position.y+1)].can_enter() in {1,3}:
					self.visible_tiles.append((int(self.position.x - 1), int(self.position.y+1)))
					if self.grid[int(self.position.x - 2)][int(self.position.y + 1)].can_enter() in {1,3}:
						self.visible_tiles.append((int(self.position.x - 2), int(self.position.y + 1)))
					if self.grid[int(self.position.x - 2)][int(self.position.y + 2)].can_enter() in {1,3}:
						self.visible_tiles.append((int(self.position.x - 2), int(self.position.y + 2)))
			if self.grid[int(self.position.x)][int(self.position.y-1)].can_enter() in {1,3}:
				self.visible_tiles.append((int(self.position.x), int(self.position.y-1)))
				if self.grid[int(self.position.x -1)][int(self.position.y-1)].can_enter() in {1,3}:
					self.visible_tiles.append((int(self.position.x -1), int(self.position.y-1)))
					if self.grid[int(self.position.x -2)][int(self.position.y + 2)].can_enter() in {1,3}:
						self.visible_tiles.append((int(self.position.x - 2), int(self.position.y -1)))
					if self.grid[int(self.position.x - 2)][int(self.position.y - 2)].can_enter() in {1,3}:
						self.visible_tiles.append((int(self.position.x - 2), int(self.position.y - 2)))
			if self.grid[int(self.position.x-1)][int(self.position.y)].can_enter() in {1,3}:
				self.visible_tiles.append((int(self.position.x-1), int(self.position.y)))
				if self.grid[int(self.position.x-2)][int(self.position.y)].can_enter() in {1,3}:
					self.visible_tiles.append((int(self.position.x-2),int(self.position.y)))
