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
from In_Terface import In_Terface

class In_Terface_Temporal(In_Terface):

	#null
	def main_loop(self):

		#unpack variables
		number_obj = len(self.pygame_rectangles)
		screen = self.screen
		scale = self.scale

		#define variables
		self.calculate_f()
		running = True
		white = (255, 255, 255)
		clock = pygame.time.Clock()
		self.time = 0


		while running:
		
			#Make the program stop when you close the window
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running = False
					sys.exit("Error")


			
			self.update_state()
				
			self.show_state(self.state)

			self.time += 0.2
			pygame.display.set_caption("Time: " + str(self.time))
			pygame.display.flip()
			clock.tick(self.FPS)
			

	
	def update_state(self):
		Ah = self.Ah
		J = self.J
		h = 100.0/(J+1)
		h_t = 0.2

		self.calculate_f()
		z = np.zeros([J, J])
		z += self.state * (1 - 4*h_t / h**2)
		z += h_t*self.F

		for i in range(J):
			for j in range(J):

				if i + 2 < J:
					z[i][j] += self.state[i+2][j] * h_t / h**2
				if j + 2 < J:
					z[i][j] += self.state[i][j+2] * h_t / h**2
				if i - 2 >= 0:
					z[i][j] += self.state[i-2][j] * h_t / h**2
				if j - 2 >= 0:
					z[i][j] += self.state[i][j-2] * h_t / h**2
					

		self.state = z