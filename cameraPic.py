#Take camera setup - 5 second sleep time/warning before picture taken

import cv2
import time 
import os

#Create object for video capturing
cam=cv2.VideoCapture(0) #Object for video capturing

#Set resolution based on Logitech Camera capabilities
cam.set(3, 1920) 
cam.set(4, 1080)
#i = 0 #Set i for naming convention used in saving images

pic_counter=0 #For filename purposes

def take_picture(pic_counter):
    print("Taking picture in 5 seconds!")
    time.sleep(5)
    ret, image=cam.read() #Live view of camera frame
    print("Taking picture now!")
    time.sleep(1)
    pic_counter = 1    
    cwd = os.getcwd()

    imagefilename = os.path.join(cwd, f'test_{pic_counter}.jpg') #Save picture to current directory 
    cv2.imwrite(imagefilename, image)  # Save picture to the rpi

take_picture(pic_counter)
pic_counter=pic_counter+1   

