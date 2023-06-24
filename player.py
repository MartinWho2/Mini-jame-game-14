import pygame
from animated_item import Animated_Item
from exit_door import Exit_Door
class Player(Animated_Item):
	def __init__(self, window, original_position, grid, offset: pygame.Vector2, towers: pygame.sprite.Group):
		self.towers = towers
		reverse_image = pygame.image.load('Images/Reverse_Idle.png')
		reverse_image =  pygame.transform.scale(reverse_image, (reverse_image.get_width()*4, reverse_image.get_height()*4))
		super().__init__(window, 'player', original_position, ['Idle','WalkingLeft','WalkingRight', 'WalkingUp', 'WalkingDown', 'power'], [True, True, True, True, True, False], grid, offset, reverse_image)

		self.death_sound = pygame.mixer.Sound('sounds/Death.wav')

		self.number_of_reverses = 0
		self.winning = False

	def move(self, direction):
		self.direction = direction
		next_cell = self.grid[int((self.position + self.direction).y)][int((self.position + self.direction).x)].can_enter()
		print("next cell: ", next_cell)
		if self.grid[int((self.position + self.direction).y)][int((self.position + self.direction).x)].__class__.__name__== 'Exit_Door':
			self.winning = True
		if next_cell in {1,4,7,9,10}:
			self.grid[int(self.position.y)][int(self.position.x)].leave(self)
			self.grid[int((self.position + self.direction).y)][int((self.position + self.direction).x)].enter(self)
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
			if next_cell == 4:
				return 1
			elif next_cell == 7:
				if not self.grid[int(self.position.y)][int(self.position.x)].get_hole().filled:
					return 1
			elif next_cell == 10:
				self.grid[int(self.position.y)][int(self.position.x)].get_flag().remove_item()
				self.number_of_reverses += 1
		elif next_cell == 2:
			following_cell = self.grid[int((self.position + 2*self.direction).y)][int((self.position + 2*self.direction).x)].can_enter()
			print("following cell:", following_cell)
			if following_cell in {1,4,7,9}:
				self.active_tile.leave(self)
				self.grid[int((self.position + self.direction).y)][int((self.position + self.direction).x)].enter(self)
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
				box = self.grid[int(self.position.y)][int(self.position.x)].get_box()
				box.move(self.direction)
				if following_cell == 7:
					hole = self.grid[int(self.position.y+self.direction.y)][int(self.position.x+self.direction.x)].get_hole()
					if not hole.filled:
						hole.fall(box)

				# In case box collides with laser
				for tower in self.towers:
					tower.update()
		else:
			print(next_cell)
			self.moving = False
		return 0

	def power(self, item):
		self.powering = True
		self.powered_item = item
		self.active_spritesheet = 'power'

	def die(self):
		self.death_sound.play(0)

