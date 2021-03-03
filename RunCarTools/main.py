import sys
sys.path.append('../')

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