import pygame
import os
class TextButton(pygame.sprite.Sprite):
	def __init__(self,position: pygame.Vector2, image_name: str):
		super().__init__()
		whole_image = pygame.image.load(os.path.join("Images",image_name+".png"))
		self.tile_size = 64
		self.images = [pygame.surface.Surface((whole_image.get_width(),16),pygame.SRCALPHA) for i in range(2)]
		for i in range(2):
			self.images[i].blit(whole_image, (0, -i*16))
			self.images[i] = pygame.transform.scale(self.images[i],(self.images[i].get_width()*4,self.tile_size))

		self.image = self.images[0]
		self.hovering = 0
		self.rect = self.image.get_rect()
		self.rect.x = position.x* self.tile_size
		self.rect.y = position.y * self.tile_size


	def change_image(self):
		self.hovering = (self.hovering+1)%2
		self.image = self.images[self.hovering]

	def set_on(self):
		self.hovering = 1
		self.image = self.images[self.hovering]

	def set_off(self):
		self.hovering = 0
		self.image = self.images[self.hovering]

