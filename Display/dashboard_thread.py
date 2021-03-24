import sys
sys.path.append('../')

import RunCarTools.globals as state_globals
import Display.gauge as gauge 
import Display.switch as switch 
import Display.progress_bar as progress_bar

import tkinter as tk
import threading as thrd
import time


class tkApp(thrd.Thread):
    def __init__(self):
        super().__init__()
        self.root = None
        self.start()

    def cb(self):
        print("Clicked")
        print("setting global = 1")
        state_globals.MYGLOBAL += 1


    def run(self):
        # print("FUCK U ")
        # root = tk.Tk()
        # but = tk.Button(root, text="Click Me", command=self.cb)
        # but.pack()
        # root.mainloop()

        root=tk.Tk()
        # root.attributes("-fullscreen", True) #can comment out if not full screen?
        canvas=tk.Canvas(root,height=400,width=800)
        canvas.pack()

        #define gauges 


        speedometer = gauge.Gauge(canvas,(300,400), 200,input_range=(0,100), units="mph")
        fuel = gauge.Gauge(canvas,(150,200), 150,input_range=(0,192), units="V")
        current = gauge.Gauge(canvas,(450,200), 150,input_range=(0,200), units="A")

        #define buttons
        but_x = 700 
        but_offset = 100
        but_space = 100

        ignit_button = switch.Switch(canvas, "IGNIT", (but_x, but_offset+0*but_space), self.cb)
        torque_vectoring = switch.Switch(canvas, "TV", (but_x, but_offset+1*but_space), self.cb)
        performance_switch = switch.Switch(canvas, "PERF", (but_x, but_offset+2*but_space), self.cb)

        #torque on wheels progress bars 
        left_torque_wheel = progress_bar.ProgBar(canvas, (50, 300), 100, "left_wheel", 150) #center of progress bar
        right_torque_wheel = progress_bar.ProgBar(canvas, (550, 300), 100, "right_wheel", 150) #center of progress bar
        root.mainloop() 


# if __name__ == "__main__":
#     app = tkApp()
#     print("global = {}".format(state_globals.MYGLOBAL))
#     while (app.is_alive()):
#         print("global = {}".format(state_globals.MYGLOBAL))
#         time.sleep(2)

#     app.join()