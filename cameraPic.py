#Take camera setup - 5 second sleep time/warning before picture taken

import cv2

cam=cv2.VideoCapture(0) #Object for video capturing

#Set resolution based on Logitech Camera capabilities
cam.set(3, 1920) 
cam.set(4, 1080)

ret, image=cam.read() #Live view of camera frame
print("Taking picture in 5 seconds!")
time.sleep(5)
print("Taking picture now!")
time.sleep(1)
cv2.imshow('test_2',image) #Show image taken
		
cv2.imwrite('/home/raspberrypi/test_2.jpg', image) #Save picture to the rpi


# import cv2

# cam=cv2.VideoCapture(0) #Object for video capturing

# #Set resolution based on Logitech Camera capabilities
# cam.set(3, 1920) 
# cam.set(4, 1080)
# def take_pic():
#     ret, image=cam.read() #Live view of camera frame
#     print("Taking picture in 5 seconds!")
#     time.sleep(5)
#     print("Taking picture now!")
#     time.sleep(1)
#     cv2.imshow('image',image) #Show image taken
            
#     cv2.imwrite('/home/raspberrypi/test_2.jpg', image) #Save picture to the rpi`