import pygame
from animated_item import Animated_Item

class Player(Animated_Item):
	def __init__(self, window, original_position, grid):
		super().__init__(window, original_position, ['monster','WalkingLeft','WalkingRight', 'WalkingUp', 'WalkingDown'], [True, True, True, True, True], grid)
		self.type = 'player'

	def move(self, direction):
		self.direction = direction
		next_cell = self.grid[int((self.position + self.direction).x)][int((self.position + self.direction).y)].can_enter()
		if next_cell == 1:
			print("empty")
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
			print("case occupée")
			if self.grid[int((self.position + 2*self.direction).x)][int((self.position + 2*self.direction).y)].can_enter() == 1:
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
		else:
			print(next_cell)
			print("case bloquée")
			self.moving = False

	def reverse(self):
		pass

