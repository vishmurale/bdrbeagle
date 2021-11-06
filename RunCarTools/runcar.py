import sys
sys.path.append('/home/debian/Beagle_21')

from time import sleep

from pins_config import * 
from Display.dashboard import ignit_button
from torque_vectoring import *
#overide this if you want to test 
DEBUG = False 
TURNED_ON = False 

def runcar_loop():
	global TURNED_ON
	try:
		if DEBUG:
			car_on = True 
			man_bmc_frg.set(GPIO.HIGH) 

		if ignit_button.presssed and not TURNED_ON:
			TURNED_ON = True 
			print("IGNIT BUTTON PRESSED") 
			man_bmc_frg.set(GPIO.HIGH) #setting frg to high
			fault_led.set(GPIO.HIGH) #turning off fault light!
			#handle buzzer 
			hv_buzz.set(GPIO.HIGH) 
			sleep(4)
			hv_buzz.set(GPIO.LOW)
		elif not ignit_button.presssed:
			TURNED_ON = False 
			man_bmc_frg.set(GPIO.LOW) #setting frg low 

			
		if TURNED_ON:  
			#calcuate speed by averaging 2 throttle potentiometer readings
			throt_1 = throt_pot_1.read_norm()
			throt_2 = throt_pot_2.read_norm()
			
			speed_avg = float((throt_1+throt_2)/2)
			speed_avg *= 100
			
			if speed_avg > 100 or throt_1 < 0 or throt_2 < 0:
				speed_avg = 0
	
			"""
			if brake.read() == 1:
				print("BREAKING OVERRIDE") 
				speed_avg = 0
			"""
			left_weight, right_weight = TorqueVectoring.torque_vector()

			lain_thrt.set_duty(speed_avg * left_weight)
			rain_thrt.set_duty(speed_avg * right_weight)
		
			
	except:
		#turn off FRG 
		print("Stopped") 
		man_bmc_frg.set(GPIO.LOW)
		exit(1)