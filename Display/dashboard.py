import sys
sys.path.append('../')

import Display.gauge as gauge 
import Display.switch as switch 
import Display.progress_bar as progress_bar
from Utils.bamocar_serial import RMC, LMC
from tkinter import *
import random 

root=Tk()

# root.attributes("-fullscreen", True) #can comment out if not full screen?
canvas=Canvas(root,height=400,width=800)
canvas.pack()

#define gauges 
speedometer = gauge.Gauge(canvas,(300,400), 200,input_range=(0,100), units="mph")
fuel = gauge.Gauge(canvas,(150,200), 150,input_range=(0,192), units="V")
current = gauge.Gauge(canvas,(450,200), 150,input_range=(0,200), units="A")

#define buttons
but_x = 700 
but_offset = 100
but_space = 100

ignit_button = switch.Switch(canvas, "IGNIT", (but_x, but_offset+0*but_space))
torque_vectoring = switch.Switch(canvas, "TV", (but_x, but_offset+1*but_space))
performance_switch = switch.Switch(canvas, "PERF", (but_x, but_offset+2*but_space))

#torque on wheels progress bars 
left_torque_wheel = progress_bar.ProgBar(canvas, (50, 300), 100, "left_wheel", 150) #center of progress bar
right_torque_wheel = progress_bar.ProgBar(canvas, (550, 300), 100, "right_wheel", 150) #center of progress bar

def update_dash():
    pass
    left_torque_wheel.set_bar(LMC.get_normalized_current())
    right_torque_wheel.set_bar(RMC.get_normalized_current())
    avg_speed = (RMC.get_mph()+LMC.get_mph())/2
    avg_curr = (RMC.get_current()+LMC.get_current())/2
    speedometer.moveto(avg_speed)
    current.moveto(avg_curr)

    #TODO UPDATE THIS 
    fuel.moveto(150)


