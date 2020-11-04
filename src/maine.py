# This is where the main loop for the car would go. Call other systems etc

import sys
import Adafruit_BBIO.GPIO as GPIO
import modules.log as log
import modules.sensor as sensor
import modules.io as io
import modules.error as err
import systems.drivetrain as drivetrain
import systems.weefee as wifi

def init():
    if (io.is_unique_pin_set()):
        log.info("Valid pin assignments, no conflicts")
    else:
        log.critical("Pin assignment has conflicts, exiting")
        sys.exit()

    log.info("Enabling FRG") 
    io.man_bmc_frg.set(GPIO.HIGH)

    log.info("Commencing main car loop")
    loop_de_looop()

# Make sure car can drive safely.
def loop_de_looop():
    bbb_still_on = True
    while bbb_still_on:

        # I/O test code can be tested here
        # %d -- integer
        # %r -- boolean
        # %f -- float
        # print("ignition value: %d" % io.ignit_btn.read())
        # print("Attempting to ring buzzer")
        # io.hv_buzz.set(True)


        # log.info("Neg air: %d | tsms: %d | enabld: %d" % \
        #          (io.neg_air.read(), io.tsms.read(), err.is_car_enabled()))

        if err.is_car_enabled():
            io.man_bmc_rfe.set(True)

            if err.is_throt_good():
                drivetrain.run_cycle()
                io.fault_led.set(False)
            else:
                drivetrain.stop_throt()
                io.fault_led.set(True)
        else:
            io.man_bmc_rfe.set(False) 
            io.fault_led.set(False) #i presumse sets led light off

if __name__ == '__main__':
    init()
