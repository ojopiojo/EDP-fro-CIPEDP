import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LogNorm
from scipy import signal

class Saved_State:

	#null
	def __init__(self, screen_size, obstacles = [], initial_values = []):

		#store scalars
		self.screen_size = screen_size

		#store array-like
		self.obstacles = obstacles
		self.initial_values = initial_values

	def get_screen_size(self):

		return self.screen_size


