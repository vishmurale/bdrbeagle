import logging as log
import Adafruit_BBIO.GPIO as GPIO
import modules.io as io

def is_throt_good(): #checking that throttle values aren't devitaing from each other
    pot_norm_1 = io.throt_pot_1.read_norm()
    pot_norm_2 = io.throt_pot_2.read_norm()

    if (pot_norm_1 < 0) or (pot_norm_2 < 0):
        return False

    # Tolerance is 10%.
    tol = 0.1
    
    # Ignore trivial readings.

    is_safe = True

    # 0.4 is an okay threshold for error ignoring.
    if (pot_norm_1 > 0.4) and (pot_norm_2 > 0.4):
        is_safe = ((pot_norm_1 / pot_norm_2 < (1 + tol)) and
                   (pot_norm_2 / pot_norm_1 < (1 + tol)))

    if not is_safe:
        log.critical("ERROR: Throttle pot readings differ by more than 10%")

    return is_safe

def is_ignit_pressed():
    return io.ignit_btn.read() == GPIO.LOW #if it's pressed, it must return LOW for some reason? Check this...

def is_car_enabled():
    if (io.neg_air.read() == GPIO.LOW) and (io.tsms.read() == GPIO.HIGH): #neg_airs something...pressure sensor?
        if is_ignit_pressed():
            is_car_enabled.on_state = True
    else:
        is_car_enabled.on_state = False

    return is_car_enabled.on_state

is_car_enabled.on_state = False
