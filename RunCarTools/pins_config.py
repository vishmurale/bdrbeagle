import sys
sys.path.append('../')
import Utils.pins 
from Utils.pins import *


# Pedal Box
throt_pot_1 = AnalogPot('P9_39', 0.144, .2, 0.46, 0.5)
throt_pot_2 = AnalogPot('P9_37', 0.03, 0.05, 0.41, 0.5)
brake = AnalogPot('P9_35', 0.05, 0.1, 0.9, 0.95)

# Dashboard
# ignit_btn = DigitalIn('P8_12', pullup=True)
# perf_switch = DigitalIn('P8_10', pullup=True)
# torq_vec = DigitalIn('P8_7', pullup=True)
fault_led = DigitalOut('P8_8')

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
lain_thrt = DigitalPWM('P9_21')
rain_thrt = DigitalPWM('P9_22')
r_rdy = DigitalIn('P8_15')
l_rdy = DigitalIn('P8_17')