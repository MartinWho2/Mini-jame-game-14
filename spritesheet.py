import os.path
import pygame, json

class Spritesheet:
	def __init__(self, filename_or_image, play_again=True, animation=True):
		self.animated = animation
		if animation:
			self.whole_image = pygame.image.load(os.path.join("Images", filename_or_image + ".png")).convert_alpha()
			json_file = json.load(open(os.path.join("Images", filename_or_image + ".json"), "r"))
			self.frames = {}
			for i in range(len(json_file["frames"].keys())):
				index = i
				frame = json_file["frames"][str(index)]["frame"]
				coordinates = pygame.rect.Rect(frame["x"],frame["y"],frame["w"],frame["h"])
				duration = json_file["frames"][str(index)]["duration"]
				frame_image = pygame.surface.Surface((coordinates.w,coordinates.h),pygame.SRCALPHA)
				frame_image.blit(self.whole_image,(-coordinates.x,-coordinates.y))
				self.frames[i] = [pygame.transform.scale(frame_image,(frame_image.get_width()*4,frame_image.get_height()*4)),duration]

			self.index_in_animation = 0
			self.time_in_frame = 0
			self.index_max = len(json_file["frames"].keys())
			self.play_again = play_again
		else:
			self.whole_image = filename_or_image

	def update(self, dt: float):
		if self.animated:
			self.time_in_frame += dt
			if self.frames[self.index_in_animation][1] < self.time_in_frame:
				self.time_in_frame -= self.frames[self.index_in_animation][1]
				self.index_in_animation += 1
				if self.index_in_animation == self.index_max:
					if self.play_again:
						self.index_in_animation = 0
					else:
						self.reset()
						return None
			return self.frames[self.index_in_animation][0]
		else:
			return self.whole_image

	def reset(self):
		self.index_in_animation = 0
		self.time_in_frame = 0

	def rotate_spritesheet(self,angle):
		if self.animated:
			for i in range(len(self.frames.keys())):
				self.frames[i][0] = pygame.transform.rotate(self.frames[i][0],angle)
		else:
			self.whole_image = pygame.transform.rotate(self.whole_image,angle)