#!/usr/bin/python

from bamo_serial import RMC, LMC
from time import sleep 

while True: 
        print("Right: ")
        print("Speed (mph): ", RMC.get_mph())
        print("Current: ", RMC.get_current())
        print("Normalized: ", RMC.get_normalized_current())

        print("================")
        print("Left: ")
        print("Speed (mph): ", LMC.get_mph())
        print("Current: ", LMC.get_current())
        print("Normalized: ", LMC.get_normalized_current())
        sleep(1)