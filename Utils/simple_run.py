import sys
sys.path.append('/home/debian/Beagle_21')

from time import sleep

from RunCarTools.pins_config import * 

while True:
	try:

		man_bmc_frg.set(GPIO.HIGH) 		


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

		lain_thrt.set_duty(speed_avg)
		rain_thrt.set_duty(speed_avg)
		
	except:
		#turn off FRG 
		print("Stopped") 
		man_bmc_frg.set(GPIO.LOW)
		exit(1)