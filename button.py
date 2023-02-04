import pygame
class Button(pygame.sprite.Sprite):
	def __init__(self, images: list[pygame.surface.Surface], position: pygame.Vector2, actionable: pygame.sprite.Sprite):
		super().__init__()
		self.images = images
		self.image = self.images[0]

