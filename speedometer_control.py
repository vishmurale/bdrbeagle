import Adafruit_BBIO.PWM as PWM
import sys 
import time 

#https://adafruit-bbio.readthedocs.io/en/latest/PWM.html
#https://www.mathworks.com/help/supportpkg/beagleboneio/ug/the-beaglebone-black-pwm-1.html
#https://learn.adafruit.com/setting-up-io-python-library-on-beaglebone-black/pwm

# Digital output pwm
class DigitalPWM():
    def __init__(self, pin, freq=100, pol=0):
        self.pin = pin
        self.freq = freq
        self.pol = pol
        PWM.start(self.pin, 0, self.freq)
    
    def set_freq(self, freq_a):
        PWM.set_frequency(self.pin, freq_a)
    
    def set_restart(self, freq_a):
        PWM.stop(self.pin)
        PWM.start(self.pin, 0, freq_a) 
        PWM.set_duty_cycle(self.pin, 90) 
    
    def set(self, duty):
        PWM.set_duty_cycle(self.pin, duty)

    def stop(self):
        PWM.stop(self.pin)


PWM.stop("P9_21")
PWM.stop("P9_22")
PWM.stop("P9_14")
PWM.stop("P8_13")
PWM.stop("P8_19") 

PWM.cleanup()
time.sleep(1)

speedometer = DigitalPWM('P8_13') #P9_14
fuel  = DigitalPWM('P9_14') #P9_14

speedometer.set(90)
fuel.set(90)

time.sleep(1)


while True:
    try: 
        freq = input("Type a freq to test")
        freq_float = int(freq)
        print("setting",freq_float) 
    
        speedometer.set_freq(freq_float)
        fuel.set_freq(freq_float)
    
    except: 
        print("EXITING")
        speedometer.stop()
        fuel.stop() 
        PWM.cleanup()
        sys.exit()


	
	
	
	

	

				
