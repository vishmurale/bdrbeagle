import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM
import Adafruit_BBIO.ADC as ADC
import time
from time import sleep


# Digital input reading
class DigitalIn():
        def __init__(self, pin, pullup=False):
                self.pin = pin
                if pullup:
                    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
                else:
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
    def __init__(self, pin, freq=2000, pol=0):
        self.pin = pin
        self.freq = freq
        self.pol = pol
        PWM.start(self.pin, 0, self.freq)
    
    def set_freq(self, freq_a):
        PWM.set_frequency(self.pin, freq_a)
    
    def set_duty(self, duty):
        PWM.set_duty_cycle(self.pin, duty)

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

               # print(pot_val)

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
PWM.cleanup()

# Pedal Box
throt_pot_1 = AnalogPot('P9_39', 0.03, 0.07, 0.38, 0.5)
throt_pot_2 = AnalogPot('P9_37', 0.12, 0.17, 0.46, 0.6)
brake = AnalogPot('P9_35', 0.05, 0.1, 0.9, 0.95)


# Dashboard
ignit_btn = DigitalIn('P8_12', pullup=True)
perf_switch = DigitalIn('P8_10', pullup=True)
torq_vec = DigitalIn('P8_7', pullup=True)
fault_led = DigitalOut('P8_8')
#speed_sig = DigitalPWM('P8_19')
#fuel_sig = DigitalPWM('P8_13')


# Accumulator
#neg_air = DigitalIn('P8_14')
#state_charge = AnalogIn('P9_40')
tsms = DigitalIn('P8_18')
#cont_req = DigitalIn('P8_16')


# Buzzer
hv_buzz = DigitalOut('P8_26')


#Torque Vectoring
steering_pot = AnalogIn('P8_38')


# Bamocar Manual
man_bmc_frg = DigitalOut('P9_23')
#lain_thrt = DigitalPWM('P9_21')
#rain_thrt = DigitalPWM('P9_22')
r_rdy = DigitalIn('P8_15')
l_rdy = DigitalIn('P8_17')
#rfe is always 12V


"""
Useful Functions related to IO
"""


car_on = False
print("CAR NOT RUNNING")



#speed_sig.set_duty(90)
#fuel_sig.set_duty(90) 



#speedometer_2.set(70)

"""
while True: 
    freq = input("Type a freq to test")
    freq_float = int(freq)
    print("setting",freq_float) 
   # speed_sig.set_freq(freq_float)
    fuel_sig.set_freq(freq_float)
"""



hv_buzz.set(GPIO.LOW)
"""
while True:
    hv_buzz.set(GPIO.HIGH)

    print("Ignit Btn Val: ", ignit_btn.read())
    print("Perf Switch Val: ", perf_switch.read())
    print("Torque Vector Val: ", torq_vec.read())

    print("running.....")
    value = input('Enter Toggle: ')
    
    if value == "FRG":
            man_bmc_frg.set(GPIO.HIGH)
            print("FRG set high")
            
    if value == "FRG!":
            man_bmc_frg.set(GPIO.LOW)	
            print("FRG set low")
    
    print("running.....")
    if ignit_btn.read() == 0:
        print("IGNIT BUTTON PRESSED") 
        car_on = not(car_on)
        man_bmc_frg.set(GPIO.HIGH) #setting frg to high
        fault_led.set(GPIO.HIGH) #turning off fault light!
        time.sleep(4)

       
    if car_on:  
         #calcuate speed by averaging 2 throttle potentiometer readings
         throt_1 = throt_pot_1.read_norm()
         throt_2 = throt_pot_2.read_norm()
         speed_avg = float((throt_1+throt_2)/2)
         speed_avg *= 100
         
         if speed_avg > 100 or throt_1 <= 0 or throt_2 <= 0:
             print("THROTTLE READ ERROR") 
             speed_avg = 0

         if brake.read() == 1:
             print("BREAKING OVERRIDE") 
             speed_avg = 0

         print(speed_avg) 
         print("Brake: ", brake.read())
         #man_bmc_frg.set(GPIO.HIGH)
         lain_thrt.set_duty(speed_avg)
         rain_thrt.set_duty(speed_avg)
    print("TSMS: ", tsms.read())
    
    

""" 
