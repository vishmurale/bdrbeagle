#!/usr/bin/python
"""
This program reads from the bamocar serial input.
Codes taken from RS232-Communication.pdf 
"""
import serial
import time
import math 
import sys

DIAMETER = 20.5
SPEED_DIVISOR = 32767 
SPEED_ACTUAL_CMD = "3D0030X".encode() #serial cmd to get speed
SPEED_RPMMAX_INT_CMD = "3D00CEX".encode() #serial cmd to get speed rpm max 

CURRENT_ACTUAL_CMD = "3D0020X".encode() #serial cmd to get current 
CURRENT_DEVICE_CMD = "3D00C6X".encode() #serial cmd to get the current_device 
CURRENT_200PC_CMD = "3D00D9X".encode() 

LOGICMAP_ERRORS_CMD = "3D008FX".encode() #serial cmd to get logicmap errors  (NOTE: Doesn't seem to really work)
LOGICMAP_IO_CMD = "3D00D8X".encode() #serial cmd to get statuses (rfe, frg, etc.) 


class SerialMotorController:
    
    def __init__(self, port):
        self.port = port 
        self.connection = serial.Serial(port=self.port, baudrate=115200)
        
        self.SPEED_RPMMAX_INT = self.write_read(SPEED_RPMMAX_INT_CMD)
        self.CURRENT_DEVICE = self.write_read(CURRENT_DEVICE_CMD)
        self.CURRENT_200PC = self.write_read(CURRENT_200PC_CMD)
        #print("Params: SPEED_RPMMAX_INT: ", self.SPEED_RPMMAX_INT)

        
    def write_read(self, cmd):
        self.connection.write(cmd)
        byte1 = self.connection.read()
        byte2 = self.connection.read() #convert binary to integer
        res = byte2 + byte1
        val = int.from_bytes(res, byteorder="big", signed=True) # We convert res from binary to a signed int
        return val
    
    def get_logic_errors(self):
        # Values it reads are nonsense for now
        cmd = LOGICMAP_ERRORS_CMD
        self.connection.write(cmd)
        byte1 = self.connection.read()
        byte2 = self.connection.read() #convert binary to integer
        bitmap = byte2 + byte1
        print(bitmap)
        val = int.from_bytes(bitmap, byteorder="big", signed=True)
        LOGICMAP_ERRORS_TABLE = [
            "bad config",
            "power fault",
            "safety",
            "field-bus timeout",
            "feedback",
            "power voltage",
            "temperature-motor",
            "temperature-device",
            "overvoltage",
            "current",
            "raceaway",
            "",
            "",
            "",
            "software",
            "bleeder"
        ]
        error_codes = []
        for i in range(0,16):
            if ((val & (1 << i)) > 0):
                print("bit set: ", i)
                code = LOGICMAP_ERRORS_TABLE[i] 
                error_codes.append(code)
        return error_codes
    
    def get_speed(self):
        speed_actual = self.write_read(SPEED_ACTUAL_CMD)
        n_act = (speed_actual/SPEED_DIVISOR)*self.SPEED_RPMMAX_INT
        return n_act
    
    def get_mph(self):
        speed_motor = self.get_speed()
        mph = (speed_motor/4.0)*DIAMETER*math.pi*60*(1.578/100000) # TO CHANGE once tire radius is known
        return abs(mph) 
    
    def get_current(self):
        curr_actual = self.write_read(CURRENT_ACTUAL_CMD)
        i_act = (curr_actual/self.CURRENT_200PC)*.2*self.CURRENT_DEVICE
        return abs(i_act)
    
    def get_normalized_current(self):
        curr_actual = self.write_read(CURRENT_ACTUAL_CMD)
        i_percentage = 200*curr_actual/self.CURRENT_200PC
        return abs(i_percentage)
    
    
RMC = SerialMotorController("/dev/ttyUSB0") #TO CONFIRM 0 or 1
LMC = SerialMotorController("/dev/ttyUSB1")
