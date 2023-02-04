import pygame
from animated_item import Animated_Item

class Player(Animated_Item):
	def __init__(self, window, original_position, grid):
		super().__init__(window, original_position, ['monster','WalkingLeft','WalkingRight', 'WalkingUp', 'WalkingDown'], [True, True, True, True, True], grid)
		self.type = 'player'

	def move(self, direction, item_list):
		pushing = False
		blocked = False
		if self.direction == (-1, 0):
			if self.position.x > 0:
				self.active_spritesheet = "WalkingLeft"
			else:
				blocked = True
		elif self.direction == (1, 0):
			if self.position.x < 9:
				self.active_spritesheet = "WalkingRight"
			else:
				blocked = True
		elif self.direction == (0, -1):
				if self.position.y > 0:
					self.active_spritesheet = "WalkingUp"
				else:
					blocked = True
		elif self.direction == (0, 1):
			if self.position.y < 9:
				self.active_spritesheet = "WalkingDown"
			else:
				blocked = True


		for item in item_list:
			if item.type == 'box':
				if (self.position+direction).x == item.position.x and (self.position+direction).y == item.position.y:
					pushing = True
					if 1<(self.position+direction).x<8 or not 1<(self.position+direction).y<8:
						for item2 in item_list:
							if item2.type == 'box':
								if (self.position + 2*direction).x == item.position.x and (self.position + 2*direction).y == item.position.y:
									blocked = True
					else:
						blocked = True

					if not blocked:
						self.position += direction
						self.moving = True
						item.move(self.direction)
					else:
						print("blocked")
						self.active_spritesheet = "monster"
		if not pushing:
			self.position += direction
			self.moving = True

	def use_reverse(self, object_to_reverse):
		pass

