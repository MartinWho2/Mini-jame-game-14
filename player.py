import pygame
from animated_item import Animated_Item
from exit_door import Exit_Door
class Player(Animated_Item):
	def __init__(self, window, original_position, grid, offset: pygame.Vector2):
		reverse_image = pygame.image.load('Images/Reverse_Idle.png')
		reverse_image =  pygame.transform.scale(reverse_image, (reverse_image.get_width()*4, reverse_image.get_height()*4))
		super().__init__(window, 'player', original_position, ['Idle','WalkingLeft','WalkingRight', 'WalkingUp', 'WalkingDown'], [True, True, True, True, True], grid, offset, reverse_image)

	def move(self, direction):
		self.direction = direction
		next_cell = self.grid[int((self.position + self.direction).x)][int((self.position + self.direction).y)].can_enter()
		if next_cell == 1:
			self.grid[int(self.position.x)][int(self.position.y)].leave(self)
			self.grid[int((self.position + self.direction).x)][int((self.position + self.direction).y)].enter(self)
			if self.direction == (-1, 0):
				self.active_spritesheet = "WalkingLeft"
			elif self.direction == (1, 0):
					self.active_spritesheet = "WalkingRight"
			elif self.direction == (0, -1):
					self.active_spritesheet = "WalkingUp"
			elif self.direction == (0, 1):
				self.active_spritesheet = "WalkingDown"

			self.position += direction
			self.movements.append(self.direction)
			self.moving = True
		elif next_cell == 2:
			if self.grid[int((self.position + 2*self.direction).x)][int((self.position + 2*self.direction).y)].can_enter() in {1,4,5}:
				self.active_tile.leave(self)
				self.grid[int((self.position + self.direction).x)][int((self.position + self.direction).y)].enter(self)
				if self.direction == (-1, 0):
					self.active_spritesheet = "WalkingLeft"
				elif self.direction == (1, 0):
					self.active_spritesheet = "WalkingRight"
				elif self.direction == (0, -1):
					self.active_spritesheet = "WalkingUp"
				elif self.direction == (0, 1):
					self.active_spritesheet = "WalkingDown"
				self.position += direction
				self.movements.append(self.direction)
				self.moving = True
				box = self.grid[int(self.position.x)][int(self.position.y)].get_box()
				box.move(self.direction)

				# In case box collides with laser
				for tower in self.towers:
					tower.update()
		else:
			print(next_cell)
			self.moving = False

