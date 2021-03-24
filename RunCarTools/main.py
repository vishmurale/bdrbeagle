import sys
sys.path.append('/home/debian/Beagle_21')

from time import sleep 
for i in range(0,60):
    print("Loading...",i,"/ 60")
    sleep(1)
    
import subprocess
subprocess.call(["sh","/home/debian/Beagle_21/run_sudo.sh"])

# from Display.dashboard import root, speedometer
from runcar import runcar_loop
from time import sleep
from Display.dashboard import root, update_dash 

while True:
    try: 
        root.update_idletasks()
        root.update()
    except:
        print("Shit crashed but we will keep going!") 
        pass 
    runcar_loop()
    update_dash()
