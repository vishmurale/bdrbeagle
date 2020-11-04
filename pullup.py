import Adafruit_BBIO.GPIO as GPIO
import time

GPIO.setup("P8_12", GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
	if GPIO.input("P8_12") == 0:
	   print("Ignit_BUTTON PRESSED")
	   time.sleep(0.1)

