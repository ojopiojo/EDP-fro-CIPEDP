import numpy as np
import pygame
import smtplib, ssl
import pickle
from pathlib import Path
import tkinter as tk
import sys
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from Inquiry import *
from Button import *
from Saved_State import Saved_State
from Object import *
from scipy import sparse
from scipy.sparse.linalg import dsolve

class In_Terface:

	#null
	def __init__(self):

		self.FPS = 20
		self.screen_x_min = 100
		self.screen_y_min = 10	
		self.scale = 5

	#null
	def initialize_interface(self):


		self.setup_buttons()
		
		self.load_objects()
		self.calculate_screen_limits()
		
		self.initialize_window()
		self.main_loop()

		self.quit()

	#null
	def setup_buttons(self):
		save_pos = (10, 12)
		add_pos = (10, 40)

		button_dimensions = (70, 20)

		save_message = "Garder"
		add_message = "Rajouter"

		green = (0, 200, 0)
		brigth_green = (0, 255, 0)

		self.save_button = Button(save_pos, button_dimensions, green, brigth_green, save_message)
		self.add_button = Button(add_pos, button_dimensions, green, brigth_green, add_message)

	#null
	def load_objects(self):

		config = Path('saved_state.txt')

		#if there's a saved state
		if config.is_file():

			with open("saved_state.txt", "rb") as f:
				self.saved_state = pickle.load(f)
			
			obstacles = self.saved_state.obstacles
			number_obs = len(obstacles)

			if number_obs > 0:

				self.pygame_rectangles = obstacles

			else: 

				self.pygame_rectangles = []

			self.screen_size = self.saved_state.get_screen_size()

			for i in range(number_obs):
				self.pygame_rectangles[i].position = self.adjust_by_margin(self.pygame_rectangles[i].position)
		

		#if not ask user for details
		else:

			self.pygame_rectangles = []
			self.screen_size = self.perform_window_inquiry()
			self.saved_state = Saved_State(self.screen_size)

		self.n = self.screen_size[0] // self.scale
		self.m = self.screen_size[1] // self.scale

		self.J = self.m
		J = self.J
		h = 1/(J+1)

		diagonal_T = np.ones(J**2)*4.0

		side_diagonal_T = np.ones(J**2-1)*(-1.0)
		side_diagonal_T[np.arange(1,J**2)%J==0] = 0

		diagonal_I = np.ones(J**2-J)

		h2_Ah = sparse.diags([-diagonal_I,
		                      side_diagonal_T,
		                      diagonal_T,
		                      side_diagonal_T,
		                      -diagonal_I],
		                     [-J,-1,0, 1,J], format="csr")

		self.Ah = h2_Ah*(1/(h**2))
		self.state = np.zeros((self.n,self.m))

	#Calculate the heat source
	def calculate_f(self):
		scale = self.scale
		self.F = np.zeros((self.n, self.m))
		number_obj = len(self.pygame_rectangles)
		for i in range(number_obj):
			x, y = self.remove_margin(self.pygame_rectangles[i].position)
			x = x // scale
			y = y // scale

			obj_length, obj_heigth = self.pygame_rectangles[i].size
			self.F[x:(x + obj_length // scale), y:(y + obj_heigth // scale)] = self.pygame_rectangles[i].value

	#null
	def calculate_screen_limits(self):
		screen_size = self.screen_size
		left = 100
		right = 10
		upper = 10
		lower = 10

		self.show_screen_size = (screen_size[0] + left + right, max(screen_size[1] + upper + lower, 100))
		self.screen_x_max = screen_size[0] + left
		self.screen_x_min = left
		self.screen_y_max = screen_size[1] + lower
		self.screen_y_min = lower

	#pos
	def adjust_by_margin(self, pos):

		return (pos[0] + self.screen_x_min, pos[1] + self.screen_y_min)

	#pos
	def remove_margin(self, pos):

		return (pos[0] - self.screen_x_min, pos[1] - self.screen_y_min)

	#null
	def add_object(self):

		#unpack variables
		scale = self.scale

		#obtain values from user
		size, value = self.perform_object_inquiry()

		#adjust by scale and margin
		size = (size[0] * scale, size[1] * scale)
		pos = self.adjust_by_margin((0,0))

		#Add object to object list
		self.pygame_rectangles.append(Obstacle(pos, size, value))
		
	#pos, size, type
	def perform_object_inquiry(self):

		inquiry = Object_Inquiry()
		return inquiry.get()

	#screen_size
	def perform_window_inquiry(self):

		#unpack variables
		scale = self.scale

		#Create interactive window
		inquiry = Window_Inquiry()

		#Get information from user
		screen_size = inquiry.get()

		#Adjust by scale
		return (screen_size[0] * scale, screen_size[1] * scale)

	#null
	def update_saved_state(self):

		self.saved_state.screen_size = self.screen_size
		margin_x = self.screen_x_min
		margin_y = self.screen_y_min

		number_obj = len(self.pygame_rectangles)
		self.saved_state.obstacles = []
		self.saved_state.initial_values = []

		for i in range(number_obj):


			size = self.pygame_rectangles[i].get_size()
			pos = self.pygame_rectangles[i].get_coordinates()
			pos = self.remove_margin(pos)
			value = self.pygame_rectangles[i].value

			if self.pygame_rectangles[i].is_obstacle():

				self.saved_state.obstacles.append(Obstacle(pos, size, value))

			else:
				self.saved_state.initial_values.append(Initial_Value(pos, size))
				
	#null
	def save_current_state(self):

		with open("saved_state.txt", "wb") as f:
			pickle.dump(self.saved_state, f)

	#null
	def initialize_window(self):

		title = "chaleur moyen: "
		pygame.init()
		self.screen = pygame.display.set_mode(self.show_screen_size)
		pygame.display.set_caption(title)

	#null
	def quit(self):

		pass
		#pygame.quit()

	def get_state(self):

		self.update_saved_state()
		return self.saved_state


	def show_state(self, state):

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit("Error")

		screen = self.screen
		white = (255, 255, 255)
		clock = pygame.time.Clock()

		screen.fill(white)
		clock.tick(self.FPS)
		h = 5
		
		self.set_color_range(np.min(state), np.max(state))

		n, m = state.shape
		for i in range(n):
			for j in range(m):
				rect = pygame.rect.Rect(i*h + self.screen_x_min, j*h + self.screen_y_min, h, h)
				pygame.draw.rect(screen, self.color(self.state[i][j]), rect)


	def set_color_range(self, min_val, max_val):

		self.min_val = min_val
		self.max_val = max_val
		

	def black_and_white(self, n):
		min_val = self.min_val
		max_val = self.max_val
		interval = max_val - min_val

		value = int(255 * (n - min_val) / interval)


		return [value, value, value]

	def color(self, n):
		min_val = self.min_val
		max_val = self.max_val
		interval = (max_val - min_val)


		if interval == 0:
			return [255,255,255]

		if (n - min_val)*3 > 2*interval:
			n -= (2.0*interval)/3
			value = int(155 * 3 * (n - min_val) // interval)
			

			return [255 - value,0,0]

		elif (n - min_val)*3 > interval:
			n -= interval/3.0
			value = int(200 * 3 * (n - min_val) // interval)
			
			if value > 100:
				return [value + 55,value + 55,0]
			else:
				return [0,255 - value,0]

		else:
			value = int(200 * 3 * (n - min_val) // interval)
			
			if value > 100:
				return [0, value + 54, 255 - value]
			else:
				return [200 - 2*value,200 - 2*value, 255 - value]
