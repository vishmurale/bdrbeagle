import sys
sys.path.append('/home/debian/Beagle_21')

import Utils.pins 
from Utils.pins import *


# Pedal Box
throt_pot_1 = AnalogPot('P9_39', 0.2, .28, 0.69, 0.8) #old: P9_39
throt_pot_2 = AnalogPot('P9_40', 0.03, 0.11, 0.61, 0.7) #old: P9_37
#brake = AnalogPot('P9_35', 0.05, 0.1, 0.9, 0.95) #old: P9_35

# Dashboard
fault_led = DigitalOut('P9_23') #old: P8_8

# Accumulator
neg_air = DigitalIn('P8_18') #old: P8_14
state_charge = AnalogIn('P9_37') #old: P9_40
tsms = DigitalIn('P8_9') #old: P8_18
cont_req = DigitalIn('P8_10') #old: P8_16


# Buzzer
hv_buzz = DigitalOut('P9_24') #old: P8_26


#Torque Vectoring
steering_pot = AnalogIn('P9_38') #old: P8_38


# Bamocar Manual
man_bmc_frg = DigitalOut('P9_15') #old: P9_23
lain_thrt = DigitalPWM('P8_19') #old: P9_21
rain_thrt = DigitalPWM('P8_13') #old: P9_22
r_rdy = DigitalIn('P8_12') #old: P8_15
l_rdy = DigitalIn('P8_8') #old: P8_17
#rfe is always 12V