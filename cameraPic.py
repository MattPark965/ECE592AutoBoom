import cv2

cam=cv2.VideoCapture(0) #Object for video capturing

#Set resolution 
cam.set(3, 1920) 
cam.set(4, 1080)

ret, image=cam.read() #Frame from camera live view
print("Taking picture in 5 seconds!")
time.sleep(5)
print("Taking picture now!")
time.sleep(1)
cv2.imshow('test_2',image) #Show image taken
		
cv2.imwrite('/home/raspberrypi/test_2.jpg', image) #Save Picture