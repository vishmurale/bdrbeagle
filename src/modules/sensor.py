import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM
import Adafruit_BBIO.ADC as ADC

# Digital input reading
class DigitalIn():
    def __init__(self, pin):
        self.pin = pin
        GPIO.setup(pin, GPIO.IN)

    def read(self):
        return GPIO.input(self.pin)

"""
It should be noted that the default position of some pins is semantically
different from what we want it to be.

For example, say we want to turn some light on, it might be the case that we
want to send a GPIO.LOW (0) signal to it instead of a GPIO.HIGH (1). However,
requiring to keep track of each individual state can be complicated. Thus, the
default constructor parameter gives you a workaround to this. Thus in our
previous light example, you would do:

some_light = DigitalOut(pin_id, GPIO.LOW)

which makes it so that when you send it a high signal of GPIO.High, True, or 1,
it automatically converts it to a GPIO.LOW signal. In the current wiring config
some of the DigitalOuts in modules/io.py have the low state.

"""
class DigitalOut():
    def __init__(self, pin, default):
        self.pin = pin
        self.default = default
        GPIO.setup(pin, GPIO.OUT)
        
    def set(self, value):
        if self.default:
            GPIO.output(self.pin, value)
        else:
            GPIO.output(self.pin, not value)

"""
A bug I had earlier was that whenever you do a PWM.start() it begins a new file
I/O read. When you have too many open, it crashes. The work around to this
without making too many states and confusing is to simply set the PWM to a 0
output to effectively render it off.

In a more complicated schema we would want to disable and then renable the PWM.
But this would require keeping track of past PWM states.
However this is also safe. Maybe.
"""
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
        self.set(0)

#Analog input reading
class AnalogIn():
    def __init__(self, pin):
        self.pin = pin

    def read(self):
        ADC.read(self.pin) # Read twice due to some driver bug. #this returns value from 0 to 1
        return ADC.read(self.pin)

ADC.setup()  #this is the shit that actaully reads it 

class AnalogPot(AnalogIn):
    def __init__(self, pin, minL, min, max, maxL):
        AnalogIn.__init__(self, pin)
        self.minL = minL
        self.min = min
        self.max = max
        self.maxL = maxL

    def read_norm(self): #makes the input some value based on params
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

