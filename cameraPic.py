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
import os

#Create object for video capturing
cam=cv2.VideoCapture(0) #Object for video capturing

#Set resolution based on Logitech Camera capabilities
cam.set(3, 1920) 
cam.set(4, 1080)
#i = 0 #Set i for naming convention used in saving images

# def take_picture():
#     ret, image=cam.read() #Live view of camera frame
#     print("Taking picture in 5 seconds!")
#     time.sleep(5)
#     print("Taking picture now!")
#     time.sleep(1)
#     #cv2.imshow('test_'+str(j),image) #Show image taken
            
#     cv2.imwrite('/home/raspberrypi/test_'+str(j)+'.jpg', image) #Save picture to the rpi

# for j in range(3):
#     take_picture()

j = 0

def take_picture(j):
    print("Taking picture in 5 seconds!")
    time.sleep(5)
    #copter.condition_yaw(0) #Sets heading north
    ret, image=cam.read() #Live view of camera frame
    print("Taking picture now!")
    time.sleep(1)
    j = 1
    #Tarps = Check_Picture_Find_Coords(image, copter.pos_alt_rel, (copter.pos_lon,copter.pos_lat))
    # cv2.imshow('test_'+str(j),image) #Show image taken        
    cwd = os.getcwd()
#
    imagefilename = os.path.join(cwd, f'test_{j}.jpg')
    cv2.imwrite(imagefilename, image)  # Save picture to the rpi
    # if Tarps is not None: #This loop executed if tarp is found
    #     cv2.circle(image, (Tarps[0], Tarps[1]), radius = 5, color = (0, 255, 0), thickness = -1)
    #     cv2.imwrite('/home/raspberrypi/test_'+str(j)+'marked'+'.jpg', image) #Save picture to the rpi

    #     packet = {
    #                 "target_x" : Tarps[0],
    #                 "target_y" : Tarps[1]
    #               }   
    #     # convert to bytes for socket data transfer
    #     packet_bytes = json.dumps(packet).encode('utf-8')
    #     # send data to the GCS
    #     # s.sendto(packet_bytes, (gcs_ip, gcs_port))
take_picture(j)
j=j+1   

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