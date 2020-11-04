import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM
import Adafruit_BBIO.ADC as ADC

from time import sleep


# Digital input reading
class DigitalIn():
	def __init__(self, pin):
		self.pin = pin
		GPIO.setup(pin, GPIO.IN)

	def read(self):
		return GPIO.input(self.pin)

# Digital output writing
class DigitalOut():
	def __init__(self, pin):
		self.pin = pin
		GPIO.setup(pin, GPIO.OUT)
		
	def set(self, value):
		GPIO.output(self.pin, value)

# Digital output pwm
class DigitalPWM():
	def __init__(self, pin, freq=1000, pol=0):
		self.pin = pin
		self.freq = freq
		self.pol = pol
		PWM.start(self.pin, 0)
	

	def set(self, duty, freq=1000):
		
		PWM.set_duty_cycle(self.pin, duty)
		PWM.set_frequency(self.pin, freq)

	def stop(self):
		PWM.stop(self.pin)

#Analog input reading
class AnalogIn():
	def __init__(self, pin):
		self.pin = pin

	def read(self):
		ADC.read(self.pin) # Read twice due to some driver bug.
		return ADC.read(self.pin)

ADC.setup()

class AnalogPot(AnalogIn):
	def __init__(self, pin, minL, min, max, maxL):
		AnalogIn.__init__(self, pin)
		self.minL = minL
		self.min = min
		self.max = max
		self.maxL = maxL

	
	

	def read_norm(self):
		pot_val = self.read()
		if (pot_val <= self.minL) or (self.maxL <= pot_val):
			return -1
		elif (self.minL < pot_val) and (pot_val < self.min):
			return 0
		elif (self.max < pot_val) and (pot_val < self.maxL):
			return 1
		else:
			mod_val = pot_val - self.min
			return mod_val / (self.max - self.min)


pin_list = []

# Pedal Box
throt_pot_1 = AnalogPot('P9_39', 0.2544, 0.2739, 0.7800, 0.8189)
throt_pot_2 = AnalogPot('P9_37', 0.0881, 0.0959, 0.6300, 0.6656)

#newparms
throt_pot_1 = AnalogPot('P9_39', 0.11, 0.16, 0.91, 0.96)
throt_pot_2 = AnalogPot('P9_37', 0.22, 0.32, 0.69, 0.73)


brake_pot = AnalogPot('P9_35', 0.05, 0.1, 0.9, 0.95)



pin_list.append(throt_pot_1)
pin_list.append(throt_pot_2)
pin_list.append(brake_pot)

# Dashboard
brake_regen = AnalogIn('P9_38')
ignit_btn = DigitalIn('P8_12')
perf_switch = DigitalIn('P8_10')
fault_led = DigitalOut('P8_8')
speed_sig = DigitalOut('P8_19')
fuel_sig = DigitalOut('P8_13')

pin_list.append(brake_regen)
pin_list.append(ignit_btn)
pin_list.append(perf_switch)
pin_list.append(fault_led)
pin_list.append(speed_sig)
pin_list.append(fuel_sig)

# Accumulator
neg_air = DigitalIn('P8_18')
state_charge = AnalogIn('P9_40')
tsms = DigitalIn('P8_16')
# limit_low = DigitalIn('P8_18')

pin_list.append(neg_air)
pin_list.append(state_charge)
pin_list.append(tsms)
# pin_list.append(limit_low)

# Buzzer
hv_buzz = DigitalOut('P8_46')

pin_list.append(hv_buzz)

# CAN Bus
can_data = DigitalOut('P8_38')
#can_recv = DigitalIn('P8_37')

pin_list.append(can_data)
#pin_list.append(can_recv)

# Bamocar Manual
man_bmc_frg = DigitalOut('P9_25')
man_bmc_rfe = DigitalOut('P9_23')
man_throt_left = DigitalPWM('P9_21')
man_throt_right = DigitalPWM('P9_22')

pin_list.append(man_bmc_frg)
pin_list.append(man_bmc_rfe)
pin_list.append(man_throt_left)
pin_list.append(man_throt_right)

"""
Useful Functions related to IO
"""


GPIO.setup("P8_12", GPIO.IN)
GPIO.setup("P8_44", GPIO.OUT)

#seems a little barred out....
#A = DigitalIn('P8_12')
#B = DigitalIn('P8_11')
#C = DigitalIn('P8_10')
#D = DigitalIn('P8_9')
#E = DigitalIn('P8_8')
#F = DigitalIn('P8_7')
pin_to_check = []
pin_to_check.append(throt_pot_1) 
#pin_to_check.append(throt_pot_2)  
#pin_to_check.append(brake_pot)  

man_bmc_rfe.set(GPIO.HIGH) 
sleep(2)
man_bmc_frg.set(GPIO.HIGH) 

while True:
	
	print("running.....")
	value = input('Enter Toggle: ')
	
	if value == "RFE":
		man_bmc_rfe.set(GPIO.HIGH) 
		print("RFE set high")
		
	if value == "FRG":
		man_bmc_frg.set(GPIO.HIGH)
		print("FRG set high")
		
	if value == "RFE!":
		man_bmc_rfe.set(GPIO.LOW) 
		print("RFE set low")

		
	if value == "FRG!":
		man_bmc_frg.set(GPIO.LOW)	
		print("FRG set low")
	
	
	print("running.....")
	value = input('Enter Toggle: ')
	
	
	for sensor in pin_to_check:
		print("Trottle : " + str(sensor.read_norm()))  
		accel = sensor.read_norm()/2
		#takes value between 0-100
		man_throt_left.set(accel)
		man_throt_right.set(accel)


	# print(GPIO.input("P8_12"))
	# GPIO.output("P8_44", GPIO.LO