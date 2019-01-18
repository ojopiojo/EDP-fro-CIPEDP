import numpy as np
import pygame
import smtplib, ssl
import pickle
from pathlib import Path
import tkinter as tk
import sys
from Inquiry import *
from Button import *
from Saved_State import Saved_State
from Object import *
from scipy import sparse
from scipy.sparse.linalg import dsolve
from In_Terface import In_Terface

class In_Terface_Stationary(In_Terface):

	#null
	def main_loop(self):

		#unpack variables
		number_obj = len(self.pygame_rectangles)
		screen = self.screen
		save_button = self.save_button
		add_button = self.add_button
		scale = self.scale

		#define variables
		need_update = True
		running = True
		white = (255, 255, 255)
		clock = pygame.time.Clock()

		while running:
	
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running = False
					sys.exit("Error")


				elif event.type == pygame.MOUSEBUTTONDOWN:
					if event.button == 1:			
						
						#Remember layers
						for i in range(number_obj):

							if self.pygame_rectangles[i].in_collision(event.pos):

								event_pos = event.pos
								self.pygame_rectangles[i].start_drag(event_pos)
				
					#change into vector of buttons
						if save_button.in_collision(event.pos):

							save_button.push()

						if add_button.in_collision(event.pos):

							add_button.push()

				elif event.type == pygame.MOUSEBUTTONUP:

						if event.button == 1:			

							for i in range(number_obj):

								self.pygame_rectangles[i].end_drag()

							if save_button.is_pushed():

								save_button.release()
								if save_button.in_collision(event.pos):
									
									self.update_saved_state()
									self.save_current_state()

							if add_button.is_pushed():

								add_button.release()
								if add_button.in_collision(event.pos):

									self.add_object()
									need_update = True
									
				elif event.type == pygame.MOUSEMOTION:

					#traspass the within limits function to the object class giving the limits
					for i in range(number_obj):
						
						left = self.screen_x_min
						right = self.screen_x_max
						upper = self.screen_y_max
						lower = self.screen_y_min
						self.pygame_rectangles[i].offset_pos(event.pos, left, right, upper, lower)
						
						if self.pygame_rectangles[i].drag:
							need_update = True


			if need_update:
				self.update_state()
				need_update = False

			self.show_state(self.state)

			save_button.draw(screen)
			add_button.draw(screen)

			pygame.display.set_caption("T moyen: " + str(np.mean(self.state)) + " T max: " + str(np.max(self.state)))
			pygame.display.flip()
			clock.tick(self.FPS)
			
			#adjust variables
			number_obj = len(self.pygame_rectangles)


		# - end -

	def update_state(self):
		Ah = self.Ah
		J = self.J

		self.calculate_f()
		b = self.to1d(self.F)
		u = dsolve.spsolve(Ah, b)

		z = np.empty([J+2, J+2])

		for i in range(0,J+2):
		  for j in range(0,J+2):

		    n = j+J*(i-1)   # Going from two indices to one
		    
		    if i==0 or i==J+1:
		        z[i,j] = 0.0
		    if j==0 or j==J+1:
		        z[i,j] = 0.0
		    if i>0 and j>0 and i<J+1 and j<J+1:
		        z[i, j] = u[n-1]    # elements of u are numbered starting at 0

		self.state = z

	def to1d(self, M):

		n,m = self.n, self.m

		b = np.ones(m * n)

		for i in range(n):
			for j in range(m):
				b[i * m + j] = M[i][j]

		return b



	