import pygame
import smtplib, ssl
import pickle
from pathlib import Path
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename



choices = { 'Meuble', 'Article'}

# Add objects
class Inquiry():
		
	def __init__(self):

		self.root = tk.Tk()
		self.makeform()

		button = tk.Button(self.root, text = 'Creer', command=self.quit)
		button.pack()

		self.root.mainloop()

class Object_Inquiry(Inquiry):

	def quit(self):

		self.value = int(self.value_entry.get())
		self.size = (int(self.length_entry.get()), int(self.heigth_entry.get()))
		self.root.destroy()

	def makeform(self):
		mainframe = tk.Frame(self.root)
		mainframe.grid(column=0,row=0 )
		mainframe.columnconfigure(0, weight = 1)
		mainframe.rowconfigure(0, weight = 1)
		mainframe.pack(pady = 100, padx = 100)


		tk.Label(mainframe, text="value").grid(row = 3, column = 0)
		self.value_entry = tk.Entry(mainframe)
		self.value_entry.insert(0, "0")
		self.value_entry.grid(row=3, column=1)


		tk.Label(mainframe, text="Largeur").grid(row = 4, column = 0)
		self.length_entry = tk.Entry(mainframe)
		self.length_entry.grid(row=4, column=1)


		tk.Label(mainframe, text="Hauteur").grid(row = 5, column = 0)
		self.heigth_entry = tk.Entry(mainframe)
		self.heigth_entry.grid(row=5, column=1)

	def get(self):

		return self.size, self.value


class Window_Inquiry(Inquiry):

	def quit(self):

		self.screen_size = (int(self.screen_length_entry.get()), int(self.screen_heigth_entry.get()))
		self.root.destroy()

	def makeform(self):
		mainframe = tk.Frame(self.root)
		mainframe.grid(column=0,row=0 )
		mainframe.columnconfigure(0, weight = 1)
		mainframe.rowconfigure(0, weight = 1)
		mainframe.pack(pady = 100, padx = 100)
		
		tk.Label(mainframe, text="Screen length").grid(row = 1, column = 0)
		self.screen_length_entry = tk.Entry(mainframe)
		self.screen_length_entry.grid(row=1, column=1)

		tk.Label(mainframe, text="Screen heigth").grid(row = 2, column = 0)
		self.screen_heigth_entry = tk.Entry(mainframe)
		self.screen_heigth_entry.grid(row=2, column=1)


	def get(self):

		return self.screen_size