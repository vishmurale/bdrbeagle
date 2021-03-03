from tkinter import *
import math as m

class Switch():                 

    def button_pressed(self):
        self.presssed = not self.presssed
        hcolor = "green" if self.presssed else "red"
        self.button.configure(highlightbackground=hcolor, bg=hcolor, highlightcolor=hcolor, activebackground=hcolor)

    def __init__(self,canvas,name,coord):
        self.presssed = False 
        self.button = Button(canvas, text=name, command = self.button_pressed, bg='red', highlightbackground="red", activebackground="red", highlightcolor="red", height=2, width=3, font=("Verdana",20))
        canvas.create_window(coord[0], coord[1], window=self.button)  