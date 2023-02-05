import pygame
from field import Tile

class Exit_Door(Tile):
	def __init__(self, image: pygame.Surface, position:pygame.Vector2):
		super().__init__(image, False, position, True)