from gpiozero import Servo
from time import sleep
import time
servo = Servo(17)

try:
	while True:
    		servo.value = -.6
    		time.sleep(8)
		servo.value = 0
		time.sleep(8)
except KeyboardInterrupt:
	print("Program stopped")
