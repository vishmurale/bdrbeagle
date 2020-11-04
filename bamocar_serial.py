#!/usr/bin/python

"""
This program reads from the bamocar serial input.
Codes taken from RS232-Communication.pdf 
"""


import serial
import time

DEVICE = "?????????"
ser = serial.Serial(port = DEVICE, baudrate=115200)

SPEED_DIVISOR = 32767 


SPEED_ACTUAL_CMD = "3D0030X".encode() #serial cmd to get speed
CURRENT_ACTUAL_CMD = "3D0020X".encode() #serial cmd to get current 

SPEED_RPMMAX_INT_CMD = "3D00CEX".encode() #serial cmd to get speed rpm max 
CURRENT_DEVICE_CMD = "3D00C6X".encode() #serial cmd to get the current_device 
CURRENT_200PC_CMD = "3D00D9X".encode() 

LOGICMAP_ERRORS_CMD = "3D008FX".encode() #serial cmd to get logicmap errors



def write_read(cmd):
	ser.write(cmd)
	return int(ser.read(), 2) #convert binary to integer 
	
def get_logic_errors(cmd):
	ser.write(cmd)
	#TODO 
	#depends on how output looks so should print
	bit_map = ser.read()
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
	for bit in bit_map:
		bit = bit_map[i]
		code = LOGICMAP_ERRORS_TABLE[i] 
		if bit == '1' and code != "":
			error_codes.append(code)
	
	return error_codes
	
	
#get constant values first 
SPEED_RPMMAX_INT = write_read(SPEED_RPMMAX_INT_CMD)
CURRENT_DEVICE = write_read(CURRENT_DEVICE_CMD)
CURRENT_200PC = write_read(CURRENT_200PC_CMD)

while True:
	
	
	#get speed 	
	SPEED_ACTUAL = write_read(SPEED_ACTUAL_CMD)
	N_ACT = (SPEED_ACTUAL/SPEED_DIVISOR)*SPEED_RPMMAX_INT
	
	#get current 
	CURRENT_ACTUAL = write_read(CURRENT_ACTUAL_CMD)
	I_ACT = (CURRENT_ACTUAL/CURRENT_200PC)*.2*CURRENT_DEVICE
	
	#get any errors 	
	ERROR = get_logic_errors(LOGICMAP_ERRORS_CMD)
	
	print("SPEED:", N_ACT)
	print("CURRENT:", N_ACT)
	print("ERRORS:", ERROR)