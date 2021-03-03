import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM
import Adafruit_BBIO.ADC as ADC

ADC.setup()
PWM.cleanup()

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