#!/usr/bin/python3

"""
This program reads from the bamocar serial input.
Codes taken from RS232-Communication.pdf 
"""
import serial
import time
import math 

DIAMETER = 20.5
SPEED_DIVISOR = 32767 
SPEED_ACTUAL_CMD = "3D0030X".encode() #serial cmd to get speed
SPEED_RPMMAX_INT_CMD = "3D00CEX".encode() #serial cmd to get speed rpm max 

CURRENT_ACTUAL_CMD = "3D0020X".encode() #serial cmd to get current 
CURRENT_DEVICE_CMD = "3D00C6X".encode() #serial cmd to get the current_device 
CURRENT_200PC_CMD = "3D00D9X".encode() 

LOGICMAP_ERRORS_CMD = "3D008FX".encode() #serial cmd to get logicmap errors



class SerialMotorController:

	def __init__(self, port):
		self.port = port 
		self.connection = serial.Serial(port=self.port, baudrate=115200)

		self.SPEED_RPMMAX_INT = self.write_read(SPEED_RPMMAX_INT_CMD)
		self.CURRENT_DEVICE = self.write_read(CURRENT_DEVICE_CMD)
		self.CURRENT_200PC = self.write_read(CURRENT_200PC_CMD)
		
	def write_read(self, cmd):
		self.connection.write(cmd)
		return int(self.connection.read(), 2) #convert binary to integer 
		
	def get_logic_errors(self):
		cmd = LOGICMAP_ERRORS_CMD
		self.connection.write(cmd)
		bit_map = self.connection.read()
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
		for i, bit in enumerate(bit_map):
			code = LOGICMAP_ERRORS_TABLE[i] 
			if bit == '1' and code != "":
				error_codes.append(code)
		return error_codes
	
	def get_speed(self):
		speed_actual = self.write_read(SPEED_ACTUAL_CMD)
		n_act = (speed_actual/SPEED_DIVISOR)*self.SPEED_RPMMAX_INT
		return n_act

	def get_mph(self):
		speed_motor = self.get_speed()
		mph = (speed_motor/4.0)*DIAMETER*math.pi*60*(1.578/100000)
		return mph 

	def get_current(self):
		curr_actual = self.write_read(CURRENT_ACTUAL_CMD)
		i_act = (curr_actual/self.CURRENT_200PC)*.2*self.CURRENT_DEVICE
		return i_act

	def get_normalized_current(self):
		curr_actual = self.write_read(CURRENT_ACTUAL_CMD)
		i_percentage = 200*curr_actual/self.CURRENT_200PC
		return i_percentage


RMC = SerialMotorController("?")
LMC = SerialMotorController("?")