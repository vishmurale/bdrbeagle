#!/usr/bin/python

"""
This program should read from the VectorNAV using a serial port
"""


"""

VN ascii header

W = write
R = read 

add NV non-volatige
add RG register 
    
From the manual you can configure output types starts on pg. 33
    36-37 shows good example of how to set output format...
    Up until 61 explains describes different fields...
    
Section 6: 
    
    example commnds: 
        VNRFS*5F restore factory settings
        
        VNRST*4D perfroms a reset...loads all non-volatile memory

    pg. 64, should we use this asynchronous output pause and resume comand? 
    pg. 72 shows async command options


"""

import serial
import time


DEVICE = "/dev/tty.usbserial-FTXU03YV"
ser = serial.Serial(port = DEVICE, baudrate=115200, timeout=1)
#ser.write("$VNWRG,06,0*6C\r\n".encode())   #turns off all async 
#ser.write("$VNWRG,06,28*XX\r\n".encode())  #sets async. register
ser.write("$VNWRG,06,28*XX\r\n".encode())  #sets async. register

#ser.write("$VNWNV*57\r\n".encode())  #write to non-volatile memory

#custom command for velocity 
#ser.write("$VNWRG,75,3,16,01,0080*XX\r\n".encode())  #pg. 34 0080 in hex is 128 which would have a 1 in 7th poistion

ser.write("$VNWRG,75,2,16,01,0029*XX\r\n".encode())  #examle from book


#print(str(ser.read(100)))
for i in range(0, 10):
    print(str(ser.read(100)))

#ser.write("$VNWRG,75,0,16,01,0029*XX\r\n".encode())
#print(str(ser.read(100)))
#ser.write("$VNWRG,76,0,16,01,0029*XX\r\n".encode())
#print(str(ser.read(100)))
#ser.write("$VNWRG,77,0,16,01,0029*XX\r\n".encode())
#print(str(ser.read(100)))

while False:
#    ser.write('$VNRRG,18*XX\r\n'.encode())
    x = str(ser.read(100))
#    print("x:",x)
    x = x.split(",")
    
    for i in range(0, len(x)):
        elem = x[i]
        if "$VNISL" in elem:
            print("READING",x[i:i+16])
            time.sleep(1)
            #acc = x[i:i+20]
            #if len(acc) == 3:
             #   print("acc", acc)
              #  time.sleep(1)
#    time.sleep(1)

#print("MESSAGE:\n", x)
