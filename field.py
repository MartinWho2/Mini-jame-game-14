import pygame
import random
from spritesheet import Spritesheet
from box import Box
class Field:
	def __init__(self, MAP_SIZE, tile_size):
		self.MAP_SIZE = MAP_SIZE
		self.tile_size = tile_size
		self.cells = [[None for j in range(self.MAP_SIZE[0]+2)] for i in range(self.MAP_SIZE[1]+2)] # Empty 2d array
		self.MAP = pygame.surface.Surface(((self.MAP_SIZE[0] + 2) * self.tile_size, (self.MAP_SIZE[1] + 2) * self.tile_size))
		self.basic_tiles = []
		self.walls = []
		self.box_images = []
		self.leak_images = [] # Will be loaded in load_tiles
		self.corner = None
		self.load_tiles('Images/tiles.png')
		self.wallProbabilities = [48, 48, 4]
		self.groundProbabilities = [86, 5, 5, 2, 2] # For 100 tiles, 48 will be of idx[0]...

	def generate_map(self):
		# Walls
		for tileX in range(1,self.MAP_SIZE[0]+1):  # Top line
			idx = self.generate_rand_wall_idx()

			if idx == 2: # Add leak underneath wall
				self.cells[0][tileX] = Tile("pipe", True, pygame.Vector2(tileX*self.tile_size, 0), False)
				self.cells[1][tileX] = Tile(self.leak_images[0], False, pygame.Vector2(tileX*self.tile_size, self.tile_size), True)
			else:
				wall = self.walls[idx]
				self.cells[0][tileX] = Tile(wall, False, pygame.Vector2(tileX * self.tile_size, 0), False)


		for tileX in range(1,self.MAP_SIZE[0]+1):  # Bottom line
			idx = self.generate_rand_wall_idx()

			if idx == 2:  # Add leak on top of wall)
				self.cells[self.MAP_SIZE[1]+1][tileX] = Tile("pipe", True, pygame.Vector2(tileX * self.tile_size, (self.MAP_SIZE[1]+1)*self.tile_size), False)
				self.cells[self.MAP_SIZE[1] + 1][tileX].rotate(180)
				self.cells[self.MAP_SIZE[1]][tileX] = Tile(self.leak_images[2], False,
											pygame.Vector2(tileX * self.tile_size, (self.MAP_SIZE[1])*self.tile_size), True)
			else:
				wall = pygame.transform.rotate(self.walls[idx], 180)
				self.cells[self.MAP_SIZE[1]+1][tileX] = Tile(wall, False, pygame.Vector2(tileX * self.tile_size, (self.MAP_SIZE[1]+1)*self.tile_size), False)


		for tileY in range(1,self.MAP_SIZE[1]+1):  # Left line
			idx = self.generate_rand_wall_idx()

			if idx == 2:  # Add leak underneath wall
				self.cells[tileY][0] = Tile("pipe", True, pygame.Vector2(0, tileY*self.tile_size), False)
				self.cells[tileY][0].rotate(90)
				self.cells[tileY][1] = Tile(self.leak_images[1], False,
											pygame.Vector2(self.tile_size, tileY*self.tile_size), True)
			else:
				wall = pygame.transform.rotate(self.walls[idx], 90)
				self.cells[tileY][0] = Tile(wall, False, pygame.Vector2(0, tileY*self.tile_size), False)


		for tileY in range(1,self.MAP_SIZE[1]+1):  # Right line
			idx = self.generate_rand_wall_idx()
			if idx == 2:  # Add leak left to wall
				self.cells[tileY][self.MAP_SIZE[0]+1] = Tile("pipe", True, pygame.Vector2((self.MAP_SIZE[0]+1) * self.tile_size, tileY*self.tile_size), False)
				self.cells[tileY][self.MAP_SIZE[0]+1].rotate(270)
				self.cells[tileY][self.MAP_SIZE[0]] = Tile(self.leak_images[3], False,
											pygame.Vector2((self.MAP_SIZE[0]) * self.tile_size, tileY*self.tile_size), True)
			else:
				wall = pygame.transform.rotate(self.walls[idx], 270)
				self.cells[tileY][self.MAP_SIZE[0]+1] = Tile(wall, False, pygame.Vector2((self.MAP_SIZE[0]+1) * self.tile_size, tileY*self.tile_size), False)

		# Corners
		self.cells[0][0] = Tile(self.corner, False, pygame.Vector2(0, 0), False)
		self.cells[0][self.MAP_SIZE[0]+1] = Tile(pygame.transform.rotate(self.corner, -90), False, pygame.Vector2((self.MAP_SIZE[0]+1)*self.tile_size,0), False)
		self.cells[self.MAP_SIZE[1]+1][0] = Tile(pygame.transform.rotate(self.corner,90),False, pygame.Vector2(0, (self.MAP_SIZE[1]+1)*self.tile_size), False)
		self.cells[self.MAP_SIZE[1] + 1][self.MAP_SIZE[0]+1] = Tile(pygame.transform.rotate(self.corner, 180), False,
												   pygame.Vector2((self.MAP_SIZE[0]+1)*self.tile_size,( self.MAP_SIZE[1] + 1)*self.tile_size), False)

		# Ground
		for tileY in range(1, self.MAP_SIZE[1]+2):
			for tileX in range(1, self.MAP_SIZE[0]+2):
				if self.cells[tileY][tileX] is None:
					tile_image = self.basic_tiles[self.generate_rand_ground_idx()]
					self.cells[tileY][tileX] = Tile(tile_image, False,
													pygame.Vector2(tileX * self.tile_size, tileY * self.tile_size),
													True)

		for row in self.cells:
			for cell in row:
				cell.display(self.MAP)

	def generate_rand_wall_idx(self):
		rand = random.random()*sum(self.wallProbabilities)

		for i in range(len(self.wallProbabilities)):
			if rand <= sum(self.wallProbabilities[:i+1]):
				return i

	def generate_rand_ground_idx(self):
		rand = random.random()*sum(self.groundProbabilities)

		for i in range(len(self.groundProbabilities)):
			if rand <= sum(self.groundProbabilities[:i+1]):
				return i


	def update(self, dt, window):
		self.MAP.fill("black")
		for l in self.cells:
			for cell in l:
				cell.update(dt)
				cell.display(self.MAP)

		window.blit(self.MAP,(0,0))

	def load_tiles(self, filename: str):
		tile_image = pygame.image.load(filename).convert_alpha()
		for i in range(5):
			tile = pygame.surface.Surface((16,16))
			tile.blit(tile_image,(-i*16,0))
			self.basic_tiles.append(pygame.transform.scale(tile, (self.tile_size, self.tile_size)))
		for i in range(3):
			tile = pygame.surface.Surface((16,16))
			tile.blit(tile_image,(-i*16,-32))
			self.walls.append(pygame.transform.scale(tile, (self.tile_size, self.tile_size)))
		for i in range(2):
			tile = pygame.surface.Surface((16,16))
			tile.blit(tile_image,(-i*16,-48))
			self.box_images.append(pygame.transform.scale(tile, (self.tile_size, self.tile_size)))
		for i in range(4):
			tile = pygame.surface.Surface((16, 16))
			tile.blit(tile_image, (-i*16, -80))
			self.leak_images.append(pygame.transform.scale(tile, (self.tile_size, self.tile_size)))

		self.corner = pygame.surface.Surface((16,16))
		self.corner.blit(tile_image,(-64,-16))
		self.corner = pygame.transform.scale(self.corner,(self.tile_size,self.tile_size))
		

class Tile(pygame.sprite.Sprite):
	def __init__(self, filename_or_image, animation: bool, position: pygame.Vector2, walkable: bool):
		super().__init__()
		self.spritesheet = Spritesheet(filename_or_image, play_again=True, animation=animation)
		self.image = self.spritesheet.update(0)
		self.position = position
		self.walkable = walkable
		self.objects_on_it = []

	def update(self,dt) -> None:
		self.image = self.spritesheet.update(dt)

	def display(self,window: pygame.surface.Surface):
		window.blit(self.image,self.position.xy)

	def rotate(self,angle):
		self.spritesheet.rotate_spritesheet(angle)

	def can_enter(self):
		# 0 : cannot, 1: ok, 2: box on it
		if self.walkable:
			for item in self.objects_on_it:
				if item.type == 'box':
					return 2
			return 1
		return 0

	def enter(self, item):
		self.objects_on_it.append(item)
		item.active_tile = self
	def leave(self,item):
		if item in self.objects_on_it:
			self.objects_on_it.remove(item)
	def get_box(self):
		for item in self.objects_on_it:
			if item.type == 'box':
				return item
		raise TypeError
