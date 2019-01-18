import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LogNorm
from scipy import signal
import pygame

class Object:
	drag = False

	#null
	def __init__(self, position, size):
		
		#(x, y) numpy array
		self.position = position
		
		#(length, heigth) numpy array
		self.size = size

		#initialize variables
		self.offset_y = self.offset_x = 0

	#null
	def __init__(self):
		pass

	#bool
	def is_obstacle(self):

		return False

	#(length, heigth)
	def get_size(self):

		return self.size

	#(pos_x, pos_y)
	def get_coordinates(self):

		return self.position

	#null
	def scale_size(self, scale):

		self.size = (max(1, self.size[1] // scale), max(1, self.size[0] // scale))

	#null
	def scale_position(self, scale):

		self.position = (self.position[1] // scale, self.position[0] // scale)

	#null
	def start_drag(self, event_pos):
		self.drag = True
		event_x, event_y = event_pos
		x, y = self.position
		self.offset_x = x - event_x
		self.offset_y = y - event_y

	#null
	def end_drag(self):
		self.drag = False


	#null
	def offset_pos(self, event_pos, left, right, upper, lower):
		if self.drag:
			event_x, event_y = event_pos
			length, heigth = self.size


			if event_x + self.offset_x + length > right:
				x = right - length
				
			elif event_x + self.offset_x < left:
				x = left
			else:
				x = event_x + self.offset_x

			if event_y + self.offset_y + heigth > upper:
				y = upper - heigth
			elif event_y + self.offset_y < lower:
				y = lower
			else:
				y = event_y + self.offset_y

			self.position = (x, y)


	def draw(self, screen):
		
		x, y = self.position
		length, heigth = self.size

		if not self.drag:
			pygame.draw.rect(screen, self.normal_color, pygame.Rect(x, y, length, heigth))
		else:
			pygame.draw.rect(screen, self.bright_color, pygame.Rect(x, y, length, heigth))

	def in_collision(self, event_pos):

		#unpack variables
		x, y = self.position
		length, heigth = self.size

		collide = (x <= event_pos[0] <= x + length)
		collide = collide and (y <= event_pos[1] <= y + heigth)

		return collide


class Obstacle(Object):

	normal_color = [0,0,0]
	bright_color = [50,50,50]
	
	#null
	def __init__(self, position, size, value = 1):
		
		#(x, y) numpy array
		self.position = position
		
		#(length, heigth) numpy array
		self.size = size

		#initialize variables
		self.offset_y = self.offset_x = 0

		self.value = value

	def is_obstacle(self):

		return True

class Initial_Value(Object):

	normal_color = [200,200,0]
	bright_color = [200, 255, 10]

	#null
	def __init__(self, position, size, value = 1):
		
		self.position = position
		self.size = size
		self.value = value

class Entry(Object):
	normal_color = [0,200,0]
	bright_color = [0, 255, 10]
	
	#null
	def __init__(self, position, size, value):
		
		self.position = position
		self.size = size
		self.value = value

class Exit(Object):
	normal_color = [200,0,0]
	bright_color = [255,0, 10]
	#null
	def __init__(self, position, size, value):
		
		self.position = position
		self.size = size
		self.value = value