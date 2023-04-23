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
import cv2
import time
import sys
import socket
import time
print("imports Completed")

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
SERVER_IP = '127.0.0.1'  # replace with the IP address of the server
# CLIENT_IP = '10.154.60.204'  # replace with the IP address of the client
#CLIENT_IP = '10.153.14.30'  # replace with the IP address of the client WILLIAMS
CLIENT_IP = '192.168.1.224'
PORT = 5501  # replace with any available port number

# Create socket object
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # DGRAM MAKES IT UDP
s.setblocking(0)

while True:
    message = 'Hello, server!'
    s.sendto(message.encode(), (CLIENT_IP, PORT))
    time.sleep(2) 
    print("debug 🫡")
    

# Receive message from server
data = s.recv(1024)
print('Received from server:', data.decode())


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
file = "recon.waypoints_new"
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
    copter.condition_yaw(0) #Sets heading north
    ret, image=cam.read() #Live view of camera frame
    print("Taking picture now!")
    time.sleep(1)
    Tarps = Check_Picture_Find_Coords(image, copter.pos_alt_rel, (copter.pos_lon,copter.pos_lat))
    #cv2.imshow('test_'+str(j),image) #Show image taken        
    cv2.imwrite('/home/raspberrypi/test_'+str(j)+'.jpg', image) #Save picture to the rpi

    if Tarps is not None: #This loop executed if tarp is found
        cv2.circle(image, (Tarps[0], Tarps[1]), radius = 5, color = (0, 255, 0), thickness = -1)
        cv2.imwrite('/home/raspberrypi/test_'+str(j)+'marked'+'.jpg', image) #Save picture to the rpi

        packet = {
                    "target_x" : Tarps[0],
                    "target_y" : Tarps[1]
                  }   
        # convert to bytes for socket data transfer
        packet_bytes = json.dumps(packet).encode('utf-8')
        # send data to the GCS
        # s.sendto(packet_bytes, (gcs_ip, gcs_port))

def dummy_take_picture(j):
    print(j)

def tarp_centering():
    centered = False
    while not centered and TARGET_ALTITUDE>=20:
        # Read the image from the drone's camera
        ret, image=cam.read()
        #IMPLEMENT CAMERA CAPTURE HERE
        cv2.imwrite('/home/raspberrypi/centering_image.jpg', image) #Save picture to the rpi


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

        # The below sets the difference in meters by 1/10 of the pixel differences
        incremental_distance_x =  dx*.1
        incremental_distance_y =  dy*.1


        # Update the current location
        currentLocation = vehicle.location.global_relative_frame

        # Update the target location based on the calculated incremental distances
        targetLocation = get_location_metres(currentLocation, incremental_distance_x, incremental_distance_y, TARGET_ALTITUDE)

        # Command the drone to move to the updated target location
        vehicle.simple_goto(targetLocation)
        TARGET_ALTITUDE -= 2.5 
        print("Drone is moving to center over the tarp")
        time.sleep(1)



    

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

print("Exited altitude loop, sleeping for 5 seconds.")
time.sleep(5)

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


while True:
    message = 'Hello, server!'
    s.sendto(message.encode(), (CLIENT_IP, PORT))
    time.sleep(2) 
    print("debug 🫡")
    try:
        msg = s.recv(1024)
        print('Received from server:', data.decode())       
        # msg = s.recvfrom(4096)
        data = msg[0]
        gcsCmd = json.loads(data.decode('utf-8'))
        print("Command Received")
        break
    except:
        '''print("Waiting for GCS")'''


# create location object from GCS calculated coordinate
# targetCoordinate = LocationGlobalRelative(gcsCmd[0], gcsCmd[1], takeoff_alt)
# go to calculated coordinate
# copter.vehicle.simple_goto(targetCoordinate)
print("GOING TO TARGET")


#tarp centering 
tarp_centering()

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