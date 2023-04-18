#Take camera setup - 5 second sleep time/warning before picture taken

# import cv2

# cam=cv2.VideoCapture(0) #Object for video capturing

# #Set resolution based on Logitech Camera capabilities
# cam.set(3, 1920) 
# cam.set(4, 1080)

# i = 0
# ret, image=cam.read() #Live view of camera frame
# print("Taking picture in 5 seconds!")
# time.sleep(5)
# print("Taking picture now!")
# time.sleep(1)
# cv2.imshow('test_'+str(i),image) #Show image taken
		
# cv2.imwrite('/home/raspberrypi/test_'+str(i)+'.jpg', image) #Save picture to the rpi
# i = i+1

import cv2
import time 

#Create object for video capturing
cam=cv2.VideoCapture(0) #Object for video capturing

#Set resolution based on Logitech Camera capabilities
cam.set(3, 1920) 
cam.set(4, 1080)
#i = 0 #Set i for naming convention used in saving images

def take_picture():
    ret, image=cam.read() #Live view of camera frame
    print("Taking picture in 5 seconds!")
    time.sleep(5)
    print("Taking picture now!")
    time.sleep(1)
    cv2.imshow('test_'+str(j),image) #Show image taken
            
    cv2.imwrite('/home/raspberrypi/test_'+str(j)+'.jpg', image) #Save picture to the rpi

for j in range(3):
    take_picture()


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
