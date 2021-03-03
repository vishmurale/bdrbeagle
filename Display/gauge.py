from tkinter import *
import math as m

def convert_range(input_range, output_range):
    
    def converter(input_val):
        dec_val = float(input_val-input_range[0])/(input_range[1]-input_range[0])
        out_val = output_range[0]+dec_val*(output_range[1]-output_range[0])

        #if it goes above the range
        if out_val > output_range[1]:
            return output_range[1]

        #if it goes below the range
        if out_val < output_range[0]:
            return output_range[0]

        return out_val

    return converter


class Gauge():                       
    def moveto(self,value):
        RAD_DEG = m.pi/180
        deg = self.input_to_degree(value)
        x1 = self.radius-(self.radius-self.NEEDLE_TICK_OFFSET)*m.cos(deg*RAD_DEG)+self.x_off
        y1 = self.radius-(self.radius-self.NEEDLE_TICK_OFFSET)*m.sin(deg*RAD_DEG)+self.y_off
        x2 = self.radius-self.radius*m.cos(deg*RAD_DEG)+self.x_off
        y2 = self.radius-self.radius*m.sin(deg*RAD_DEG)+self.y_off

        self.central_text.configure(text=str(value)+" "+ self.units)
        self.canvas.coords(self.needle,x2,y2,x1,y1)



    def __init__(self,canvas,coordinates,radius,bg="#ffffff",needlecolor="#FF4500",markscolor="#000000",input_range=(0,200),digitscolor="#ff9933", units="mph"):
        self.needlecolor=needlecolor
        self.canvas=canvas
        self.radius = radius
        self.units = units

        cx = coordinates[0] #center of circle
        cy = coordinates[1] #center of circle 

        #generate bounding box to create arc
        bx1 = cx - self.radius
        by1 = cy - self.radius
        bx2 = cx + self.radius
        by2 = cy + self.radius
        self.canvas.create_arc(bx1, by1, bx2, by2, start=0, extent=180, style=ARC, width=3)
        
        #generate offset coordinates as left hand corner is (0,0)
        self.x_off = bx1 
        self.y_off = by1 

        self.range_marks=[]

        self.degree_to_input = convert_range((0,180), input_range) #convert degrees to input range! 
        self.input_to_degree = convert_range(input_range, (0,180)) #convert input to degree range! 

        RAD_DEG = m.pi/180
        self.NEEDLE_TICK_OFFSET = 50 #how long we want needle to be
        BIG_TICK_OFFSET = 20 #different sizes for gauge markings
        SMALL_TICK_OFFSET = 10 #different sizes for gauge markings
        q=10
        u=0
        for i in range(0,181,5):
            if(i%10==0):
                x1 = self.radius-(self.radius-BIG_TICK_OFFSET)*m.cos(i*RAD_DEG)+self.x_off 
                y1 = self.radius-(self.radius-BIG_TICK_OFFSET)*m.sin(i*RAD_DEG)+self.y_off
                x2 = self.radius-self.radius*m.cos(i*RAD_DEG)+self.x_off 
                y2 = self.radius-self.radius*m.sin(i*RAD_DEG)+self.y_off
                canvas.create_line(x1,y1,x2,y2,fill=markscolor,width=3) 
           

                # self.range_marks.append(canvas.create_text(x1,y1,text=int(self.degree_to_input(i)),font=("Courier",int(self.radius/25)),fill=digitscolor))
            else:
                x1 = self.radius-(self.radius-SMALL_TICK_OFFSET)*m.cos(i*RAD_DEG)+self.x_off
                y1 = self.radius-(self.radius-SMALL_TICK_OFFSET)*m.sin(i*RAD_DEG)+self.y_off
                x2 = self.radius-self.radius*m.cos(i*RAD_DEG)+self.x_off
                y2 = self.radius-self.radius*m.sin(i*RAD_DEG)+self.y_off
                canvas.create_line(x1,y1,x2,y2,fill="#acace6",width=2)
            
            if(i>=90):
                q=+10
                u=q
            else:
                q=10
                u=0


        #Text of gauge
        font_size = int(radius*.2)
        text_y_offset = int(.2*self.radius)

        self.central_text = Label(canvas, text='0'+" "+units, fg='black', bg='white', font=("Verdana",font_size))
        # self.central_text.pack()
        
        x = self.radius + self.x_off
        y = self.radius-text_y_offset + self.y_off 
        self.canvas.create_window(x, y, window=self.central_text)  

        #initial value of needle 
        value = 0
        deg = self.input_to_degree(value)
        x1 = self.radius-(self.radius-self.NEEDLE_TICK_OFFSET)*m.cos(deg*RAD_DEG)+self.x_off
        y1 = self.radius-(self.radius-self.NEEDLE_TICK_OFFSET)*m.sin(deg*RAD_DEG)+self.y_off
        x2 = self.radius-self.radius*m.cos(deg*RAD_DEG)+self.x_off
        y2 = self.radius-self.radius*m.sin(deg*RAD_DEG)+self.y_off
        self.needle=canvas.create_line(x2,y2,x1,y1,fill=needlecolor,width=8, arrow=FIRST)