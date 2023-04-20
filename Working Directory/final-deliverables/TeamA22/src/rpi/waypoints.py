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

# set up socket to send data to GCS
# s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# gcs_ip = args.gcs_ip
# gcs_port = int(args.gcs_port)
# rpi_port = int(args.rpi_port)
# rpi_ip = args.rpi_ip
# s.bind((rpi_ip, int(rpi_port)))

# TODO FIX SOCKET AND UNCOMMENT ABOVE CODE AFTER FIXED need a change to commit


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
Targets = []

#Reusable take picture+save image function
def take_picture():
    print("Taking picture in 5 seconds!")
    time.sleep(5)
    copter.condition_yaw(0) #Sets heading north
    ret, image=cam.read() #Live view of camera frame
    print("Taking picture now!")
    time.sleep(1)
    Tarps = Check_Picture_Find_Coords(image, copter.pos_alt_rel, (copter.pos_lon,copter.pos_lat))
    cv2.imshow('test_'+str(j),image) #Show image taken        
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
    time.sleep(1)

time.sleep(5)

copter.vehicle.airspeed = 3 #m/s
#count = 1

# parse through each waypoint in file
for j, command in enumerate(missionlist):
    # go to waypoint
    point1 = LocationGlobalRelative(command.x, command.y, command.z)
    copter.vehicle.simple_goto(point1)
    while(copter.distance_to_current_waypoint(command.x, command.y, command.z) > float(position_buffer)):
        time.sleep(0.001)
        #count = count + 1
    take_picture()
    print("GOING TO NEXT WAYPOINT")

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

# create location object from GCS calculated coordinate
# targetCoordinate = LocationGlobalRelative(gcsCmd[0], gcsCmd[1], takeoff_alt)
# go to calculated coordinate
# copter.vehicle.simple_goto(targetCoordinate)
print("GOING TO TARGET")

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
