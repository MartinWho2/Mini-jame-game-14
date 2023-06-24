import pygame
from normal_item import Normal_Item

class Button(Normal_Item):
	def __init__(self, window, linked, original_position:pygame.Vector2, images, grid, offset):
		super().__init__(window, 'button',False, original_position, images, grid, offset)
		self.linked = linked
		self.state = True #True = appuyé
		self.refresh()

		self.hover_sound = pygame.mixer.Sound('sounds/Hover_click.wav')


	def change_state(self):
		self.state = not self.state
		if self.state:
			self.hover_sound.play(0)
		self.linked.change_state()

	def refresh(self):
		items = self.grid[int(self.position.y)][int(self.position.x)].objects_on_it
		print(items)
		for item in items:
			if item.type == 'box' or item.type == 'player':
				if not self.state:
					print("changing state")
					self.change_state()
			else:
				if self.state:
					print("changing state")
					self.change_state()





