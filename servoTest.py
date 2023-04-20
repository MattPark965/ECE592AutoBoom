from gpiozero import Servo
from time import sleep
import time
servo = Servo(17)
#servo.frame_width(.5)
i = 1
try:
	while True:
		for i in range (3):
			servo.value = 1 - (i * .1)
			time.sleep(.5)
		i = 1
except KeyboardInterrupt:
	print("Program stopped")
