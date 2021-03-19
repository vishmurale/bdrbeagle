import sys
sys.path.append('/home/debian/Beagle_21')

# from Display.dashboard import root, speedometer
from runcar import runcar_loop
from time import sleep
from Display.dashboard import root, update_dash 
from time import sleep 


import subprocess
subprocess.call(["sh","./run_sudo.sh"])

while True:
    try: 
        root.update_idletasks()
        root.update()
    except:
        print("Shit crashed but we will keep going!") 
        pass 
    runcar_loop()
    update_dash()