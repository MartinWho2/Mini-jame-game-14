import pygame
import random
from spritesheet import Spritesheet

class Field:
	def __init__(self, MAP_SIZE, tile_size):
		self.MAP_SIZE = MAP_SIZE
		self.tile_size = tile_size
		self.cells = [[None for j in range(self.MAP_SIZE[0]+2)] for i in range(self.MAP_SIZE[1]+2)]
		self.MAP = pygame.surface.Surface(((self.MAP_SIZE[0] + 2) * self.tile_size, (self.MAP_SIZE[1] + 2) * self.tile_size))
		self.basic_tiles = []
		self.walls = []
		self.box_images = []
		self.leak_image = None
		self.corner = None
		self.load_tiles('Images/tiles.png')

	def generate_map(self):
		# Walls
		for tileX in range(1,self.MAP_SIZE[0]+1):  # Top line
			idx = random.randint(0, len(self.walls) - 1)

			if idx == 2: # Add leak underneath wall
				self.cells[0][tileX] = Tile("pipe", True, pygame.Vector2(tileX*self.tile_size, 0), False)
				self.cells[1][tileX] = Tile(self.leak_image, False, pygame.Vector2(tileX*self.tile_size, self.tile_size), True)
			else:
				wall = self.walls[idx]
				self.cells[0][tileX] = Tile(wall, False, pygame.Vector2(tileX * self.tile_size, 0), False)


		for tileX in range(1,self.MAP_SIZE[0]+1):  # Bottom line
			idx = random.randint(0, len(self.walls) - 1)

			if idx == 2:  # Add leak on top of wall)
				self.cells[self.MAP_SIZE[1]+1][tileX] = Tile("pipe", True, pygame.Vector2(tileX * self.tile_size, (self.MAP_SIZE[1]+1)*self.tile_size), False)
				self.cells[self.MAP_SIZE[1] + 1][tileX].rotate(180)
				self.cells[self.MAP_SIZE[1]][tileX] = Tile(pygame.transform.rotate(self.leak_image, 180), False,
											pygame.Vector2(tileX * self.tile_size, (self.MAP_SIZE[1])*self.tile_size), True)
			else:
				wall = pygame.transform.rotate(self.walls[idx], 180)
				self.cells[self.MAP_SIZE[1]+1][tileX] = Tile(wall, False, pygame.Vector2(tileX * self.tile_size, (self.MAP_SIZE[1]+1)*self.tile_size), False)


		for tileY in range(1,self.MAP_SIZE[1]+1):  # Left line
			idx = random.randint(0, len(self.walls) - 1)

			if idx == 2:  # Add leak underneath wall
				self.cells[tileY][0] = Tile("pipe", True, pygame.Vector2(0, tileY*self.tile_size), False)
				self.cells[tileY][0].rotate(90)
				self.cells[tileY][1] = Tile(pygame.transform.rotate(self.leak_image, 90), False,
											pygame.Vector2(self.tile_size, tileY*self.tile_size), True)
			else:
				wall = pygame.transform.rotate(self.walls[idx], 90)
				self.cells[tileY][0] = Tile(wall, False, pygame.Vector2(0, tileY*self.tile_size), False)


		for tileY in range(1,self.MAP_SIZE[1]+1):  # Right line
			idx = random.randint(0, len(self.walls) - 1)
			if idx == 2:  # Add leak left to wall
				self.cells[tileY][self.MAP_SIZE[0]+1] = Tile("pipe", True, pygame.Vector2((self.MAP_SIZE[0]+1) * self.tile_size, tileY*self.tile_size), False)
				self.cells[tileY][self.MAP_SIZE[0]+1].rotate(270)
				self.cells[tileY][self.MAP_SIZE[0]] = Tile(pygame.transform.rotate(self.leak_image, 270), False,
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
					tileImage = random.choice(self.basic_tiles)
					self.cells[tileY][tileX] = Tile(tileImage, False,
													pygame.Vector2(tileX * self.tile_size, tileY * self.tile_size),
													True)

		for row in self.cells:
			for cell in row:
				cell.display(self.MAP)

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
			self.basic_tiles.append(pygame.transform.scale(tile,(self.tile_size,self.tile_size)))
		for i in range(3):
			tile = pygame.surface.Surface((16,16))
			tile.blit(tile_image,(-i*16,-32))
			self.walls.append(pygame.transform.scale(tile,(self.tile_size,self.tile_size)))
		for i in range(2):
			tile = pygame.surface.Surface((16,16))
			tile.blit(tile_image,(-i*16,-48))
			self.box_images.append(tile)

		self.leak_image = pygame.surface.Surface((16, 16))
		self.leak_image.blit(tile_image,(0,-16))
		self.leak_image = pygame.transform.scale(self.leak_image, (self.tile_size, self.tile_size))

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

	def update(self,dt) -> None:
		self.image = self.spritesheet.update(dt)

	def display(self,window: pygame.surface.Surface):
		window.blit(self.image,self.position.xy)

	def rotate(self,angle):
		self.spritesheet.rotate_spritesheet(angle)