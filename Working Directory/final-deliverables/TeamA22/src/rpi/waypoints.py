'''
    Continued by:
    Wesley Cowand
    ECE 592 - Autonomous Bomber
    Ayush Luthra
    Alex Wheelis
    Kishan Joshi
    Harrison Tseng
    MavProxy:
    mavproxy.exe --master="com3" --out=udp:127.0.0.1:14450 --out=udp:127.0.0.1:14560 --out=udp:127.0.0.1:14570
    com3: UAV connected via USB
    10000: Python app
    20000: QGC
    30000: MissionPlanner
'''


from header import *
from copter import Copter
from NewDetection import Check_Picture_Find_Coords
from tarpdetector import detect_blue_cluster
import cv2
import time
import sys
import socket
import time
import os
# import MissionPlanner #import *
# # clr.AddReference(“MissionPlanner.Utilities”) # includes the Utilities class
# from MissionPlanner.Utilities import Locationwp
print("imports Completed")

cwd = os.getcwd()
# item = MissionPlanner.Utilities.Locationwp()
# alt = 30
# MissionPlanner.Utilities.Locationwp.alt.SetValue(item,alt)
# print("Altitude changed to 30 m")


# parse arguemnts from command line
parser = argparse.ArgumentParser()
parser.add_argument('--gcs_ip', default='192.168.1.148')
parser.add_argument('--gcs_port', default='4444')
parser.add_argument('--rpi_ip', default='192.168.1.147')
parser.add_argument('--rpi_port', default='5555')
parser.add_argument('--connect', default='udp:127.0.0.1:14551')
args = parser.parse_args()

# connect to copter on localhost
# import argparse
# parser = argparse.ArgumentParser(description='Commands vehicle using vehicle.simple_goto.')
# parser.add_argument('--connect', help="Vehicle connection target string.")
# args = parser.parse_args()

# aquire connection_string
connection_string = args.connect
if not connection_string:
    sys.exit('Please specify connection string')

# Connect to the Vehicle
print('Connecting to vehicle on: %s' % connection_string)
copter = Copter(connection_string)
print("CONNECTED")

# # set up socket to send data to GCS
# s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# gcs_ip = args.gcs_ip
# gcs_port = int(args.gcs_port)
# rpi_port = int(args.rpi_port)
# rpi_ip = args.rpi_ip
# s.bind((rpi_ip, int(rpi_port)))

# Set up IP addresses and port
SERVER_IP = '192.168.1.164'  # replace with the IP address of the server
# SERVER_IP = '0.0.0.0'  # replace with the IP address of the server
# CLIENT_IP = '10.154.60.204'  # replace with the IP address of the client
#CLIENT_IP = '10.153.14.30'  # replace with the IP address of the client WILLIAMS
CLIENT_IP = '192.168.1.224'
PORTpi = 6001 # replace with any available port number
PORTgcs = 5501
# Create socket object
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # DGRAM MAKES IT UDP
# s.setblocking(0)
s.bind((SERVER_IP, PORTpi))
# while True:
#     message = 'Hello, server!'
#     s.sendto(message.encode(), (CLIENT_IP, PORT))
#     time.sleep(2) 
#     print("debug 🫡")
    

# # Receive message from server
# data = s.recv(4096)
# print('Received from server:', data.decode())


# setup listeners to get all messages from the copter
copter._setup_listeners()

# give some time for all changes to take place
time.sleep(2)

# print current coordinates to check for good GPS signal
print("Bypass Here - FOR DEBUG ONLY🫡")
# print("LAT : " + str(copter.pos_lat))
# print("LON : " + str(copter .pos_lon))

# check arming status of the copter
while not copter.is_armed():
    # wait for safety pilot to arm
    print("Waiting to be armed...")
    time.sleep(1)

print("ARMED")

time.sleep(2)

# clear all missions from the copter
copter.clear_mission()

# load recon grid flight plan to copter
missionlist = []
file = "recon.waypoints_4:26"
missionlist = copter.readmission(file)

# 2m buffer for gps coordinates
position_buffer = 2

# print mission items for verification
print("MISSION LIST: \n" + str(missionlist))

#Create object for video capturing
cam=cv2.VideoCapture(0) #Object for video capturing

#Set resolution based on Logitech Camera capabilities
cam.set(3, 1920) 
cam.set(4, 1080)

#Initialize vars necessary for the tarp detection code
j = 0

#Reusable take picture+save image function
def take_picture(j):
    print("Taking picture in 5 seconds!")
    time.sleep(5)
    # copter.vehicle.condition_yaw(0) #Sets heading north
    ret, image=cam.read() #Live view of camera frame
    print("Taking picture now!")
    time.sleep(1)
    imagefilename = os.path.join(cwd, f'test_{j}.jpg')
    cv2.imwrite(imagefilename, image)  # Save picture to the rpi
    # imagefilename = f'~/ece592/ECE592AutoBoom/test_'+str(j)+'.jpg'
    # cv2.imwrite(imagefilename, image)  # Save picture to the rpi
    Tarps = Check_Picture_Find_Coords(imagefilename, copter.pos_alt_rel, (copter.pos_lon,copter.pos_lat), j)
    #cv2.imshow('test_'+str(j),image) #Show image taken        
    #cv2.imwrite('/home/raspberrypi/test_'+str(j)+'.jpg', image) #Save picture to the rpi

    if Tarps is not None: #This loop executed if tarp is found
        cv2.circle(image, (int(Tarps[0]), int(Tarps[1])), radius = 5, color = (0, 255, 0), thickness = -1)
        imagefilename = os.path.join(cwd, f'test_{j}_marked.jpg')
        cv2.imwrite(imagefilename, image)  # Save picture to the rpi
        # cv2.imwrite('~/ece592/ECE592AutoBoom/test_'+str(j)+'marked'+'.jpg', image) #Save picture to the rpi

        packet = {
                    "target_x" : Tarps[0],
                    "target_y" : Tarps[1]
                  }   
        # convert to bytes for socket data transfer
        packet_bytes = json.dumps(packet).encode('utf-8')
        # send data to the GCS
        s.sendto(packet_bytes, (CLIENT_IP, PORTgcs))

def dummy_take_picture(j):
    print(j)

def tarp_centering():
    lower_blue = np.array([80, 0, 0])  # Lower bound of the blue color range in HSV
    upper_blue = np.array([160, 75, 35])  # Upper bound of the blue color range in HSV
    j = 0
    centered = False
    while not (centered):
        # Read the image from the drone's camera
        ret, image=cam.read()
        #IMPLEMENT CAMERA CAPTURE HERE
        cwd = os.getcwd()
        # cv2.imwrite('/home/raspberrypi/centering_image.jpg', image) #Save picture to the rpi
        imagefilename = os.path.join(cwd, f'centering_image_{j}.jpg')
        cv2.imwrite(imagefilename, image)  # Save picture to the rpi

        image = cv2.imread(imagefilename)
        j+=1
        # Get the center of the tarp using the detect_blue_cluster() function
        tarp_center = detect_blue_cluster(image, lower_blue, upper_blue)

        # Define the image center
        image_center = (image.shape[1] // 2, image.shape[0] // 2)

        # Calculate the pixel difference between the image center and the tarp center
        dx = tarp_center[0] - image_center[1]
        dy = tarp_center[1] - image_center[0]

        # Check if the tarp is centered within 5% of the image dimensions
        if abs(dx) < 0.05 * image.shape[1] and abs(dy) < 0.05 * image.shape[0]:
            centered = True
            print("Tarp centered")
            continue

        # As in the Check Image Get Coords function Here is the calculated values for each pixel in meters
        PixelMetersWidth  = 0.0341
        PixelMetersHeight = 0.0455

        # The below sets the difference in meters by 1/10 of the pixel differences
        incremental_distance_x =  dx * PixelMetersWidth
        incremental_distance_y =  dy * PixelMetersHeight


        # Update the current location
        currentLocation = copter.vehicle.location.global_relative_frame

        # Update the target location based on the calculated incremental distances
        targetLocation = copter.vehicle.get_location_metres(currentLocation, incremental_distance_x, incremental_distance_y)

        # Command the drone to move to the updated target location
        copter.vehicle.simple_goto(targetLocation)

        print("Drone is moving to center over the tarp")
        time.sleep(5)

    

# set copter to guided autopilot mode
copter.set_ap_mode("GUIDED")

print("Taking off")

# setting takeoff altitude m
takeoff_alt = 50

# take off to target altitude
copter.vehicle.simple_takeoff(takeoff_alt)

# wait while copter reaches desired altitude
while copter.pos_alt_rel < takeoff_alt*0.95:
    print("Gaining altitude")
    print("/n ", copter.pos_alt_rel)
    time.sleep(1)

print("Exited altitude loop, sleeping for 2 seconds.")
time.sleep(2)
copter.condition_yaw(0) #Sets heading north
print("Setting heading, then sleeping for 5 seconds")
time.sleep(5)

# #### ------------------------ DELETE AFTER TESTING

# take_picture(22)
# print("sleeping, RTL is no errors")
# copter.set_ap_mode("RTL")
# time.sleep(200)

# #### ------------------------

# copter.vehicle.airspeed = 3 #m/s
#count = 1
print("Beginning path to first waypoint at 3 m/s")

# parse through each waypoint in file
for command in missionlist:
    # go to waypoint
    point1 = LocationGlobalRelative(command.x, command.y, command.z)
    copter.vehicle.simple_goto(point1, airspeed=10, groundspeed=10)
    print("Going to waypoint")
    while(copter.distance_to_current_waypoint(command.x, command.y, command.z) > float(position_buffer)):
        time.sleep(1)
        print(copter.distance_to_current_waypoint(command.x, command.y, command.z), float(position_buffer))
        #count = count + 1
    #dummy_take_picture(j)
    take_picture(j)
    j=j+1 
    #print("GOING TO NEXT WAYPOINT")

# set socket behavior
# s.setblocking(0)

# wait for calculated coordinates from the GCS
# while True:
#     try:
#         msg = s.recvfrom(4096)
#         data = msg[0]
#         gcsCmd = json.loads(data.decode('utf-8'))
#         print("Command Received")
#         break
#     except:
#         '''print("Waiting for GCS")'''

# print(gcsCmd)

#set socket behavior

#message = 'Hello, server!'
#s.sendto(message.encode(), (CLIENT_IP, PORT))
#time.sleep(2) 
print("debug 🫡")

#while True:
 #   try:
print("Waiting for GCS")
msg = s.recvfrom(4096)
#print('Received from server:', data.decode())       
        #msg = s.recvfrom(4096)
print(msg)
data = msg[0]
print (data)
gcsCmd = json.loads(data.decode('utf-8'))
print("Command Received")
  #      break
  #  except:
        #'''print("Waiting for GCS")'''


# create location object from GCS calculated coordinate
targetCoordinate = LocationGlobalRelative(gcsCmd[0], gcsCmd[1], 40) # drops altitude to 40 to center over target
# go to calculated coordinate
copter.vehicle.simple_goto(targetCoordinate)
print("GOING TO TARGET and sleeping for 15")
time.sleep(15)

#tarp centering 
tarp_centering()
targetCoordinate = LocationGlobal((copter.pos_lon,copter.pos_lat, 20)) # Updates targ coord to where it centered at 40m
copter.vehicle.simple_goto(targetCoordinate)
tarp_centering() # centers again at 20M

# wait while the copter is travelling to the calculated coordinate
# while(copter.distance_to_current_waypoint(gcsCmd[0], gcsCmd[1], takeoff_alt) > float(5)):
#     time.sleep(1)
#     print("Going to waypoint")

# drop bomb
copter.bomb_one_away()
print("DROPPED BOMB1")
time.sleep(2)

# set autopilot mode to RTL
copter.set_ap_mode("RTL")
