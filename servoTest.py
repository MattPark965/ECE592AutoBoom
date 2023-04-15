from gpiozero import Servo
from time import sleep

servo = Servo(17)

try:
	while True:
    		servo.value = .5
    		sleep(1)
except KeyboardInterrupt:
	print("Program stopped")
