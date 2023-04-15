from gpiozero import Servo
from time import sleep
import time
servo = Servo(17)

try:
	while True:
		#first bomb release value
    		servo.value = -.6
    		time.sleep(8)
		#second bomb release value
		servo.value = 0
		time.sleep(8)
except KeyboardInterrupt:
	print("Program stopped")
