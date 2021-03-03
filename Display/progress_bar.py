from tkinter import *
from tkinter.ttk import *
import math as m

class ProgBar():                 

    def set_bar(self, value):

        percent = float(value)/self.max_val
        index = int(percent*len(self.colors_arr)-1)
        color_code = self.colors_arr[index]
        self.progress['value'] = value
        self.bar_style.configure(self.style_name, foreground=color_code, background=color_code) #will change color
        
    def __init__(self,canvas,coord, max_val, name, length):
        
        self.colors_arr = []
        step_size = 10

        #red to yellow
        for i in range(0, 255, step_size):
            hex_clean = hex(i)[2:]
            hex_clean = "0"+hex_clean if len(hex_clean) == 1 else hex_clean
            color_code = "#ff" + hex_clean + "00"
            self.colors_arr.append(color_code)

         #Yellow to Green 
        for i in range(255, 0, -step_size):
            hex_clean = hex(i)[2:]
            hex_clean = "0"+hex_clean if len(hex_clean) == 1 else hex_clean
            color_code = "#" + hex_clean + "ff00"
            self.colors_arr.append(color_code)
    
        #reverse the array 
        self.colors_arr.reverse()

        self.name = name 
        self.max_val = max_val
        self.bar_style = Style()
        self.bar_style.theme_use("default")
        self.style_name = name+".Vertical.TProgressbar"
        self.bar_style.configure(self.style_name, foreground='green', background='green', thickness=50)
        self.progress = Progressbar(canvas, orient = VERTICAL, length = length, mode = 'determinate', maximum=max_val, style=self.style_name)
        self.progress['value'] = 0
        canvas.create_window(coord[0], coord[1], window=self.progress)   


        

