# Here goes drivetrain code

# Uses input data from various sensors (throttle pots, brake pot, steering etc)
# to send data out the CAN module

import Adafruit_BBIO.GPIO as GPIO
import modules.io as io
import modules.log as log

perf_scale = 0.5

def is_perf_on():
    return io.perf_switch.read() == GPIO.HIGH #what is perf switch?

def get_accel():
    raw_throt = (io.throt_pot_1.read_norm() + io.throt_pot_2.read_norm()) / 2
    return raw_throt if is_perf_on() else raw_throt * perf_scale

def is_brake_on():
    # log.info("Brake value: %d" % io.brake_pot.read_norm())
    # return io.brake_pot.read_norm() > 0.25
    return False #somewhat probelmatic probally should be above

def stop_throt():
    io.man_throt_left.stop()
    io.man_throt_right.stop()
    # io.man_bmc_rfe.set(GPIO.LOW)

def set_throt(left, right):
    io.man_throt_left.set(left)
    io.man_throt_right.set(right)

def run_cycle():
    # Read appropriate values from potentiometers and do appropriate writes

    if is_brake_on():
        log.info("Brake engaged")
        stop_throt()
    else:
        io.man_bmc_rfe.set(GPIO.HIGH) 
        accel = get_accel()
        set_throt(accel, accel)             #set values for accelerator based on potential #changing duty values of PWM, larger values I think mean more spead
        log.info("Throttle value: %f" % accel)

