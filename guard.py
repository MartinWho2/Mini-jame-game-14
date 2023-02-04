import pygame
from animated_item import Animated_Item

class Guard(Animated_Item):
	def __init__(self, window, original_position, grid, offset: pygame.Vector2):
		reverse_image = pygame.image.load('Images/Reverse_Idle.png')
		reverse_image = pygame.transform.scale(reverse_image,(reverse_image.get_width() * 4, reverse_image.get_height() * 4))
		super().__init__(window, original_position, ['LeGardien', 'LeGardienGauche', 'LeGardienDroite', 'LeGardienUp', 'LeGardienDown'], [True, True, True, True, True], grid, offset, reverse_image)
		self.type = 'guard'