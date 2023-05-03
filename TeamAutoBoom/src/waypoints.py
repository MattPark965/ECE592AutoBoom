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

print("imports Completed")

cwd = os.getcwd() #Get current directory


# parse arguemnts from command line
parser = argparse.ArgumentParser()
parser.add_argument('--gcs_ip', default='192.168.1.148')
parser.add_argument('--gcs_port', default='4444')
parser.add_argument('--rpi_ip', default='192.168.1.147')
parser.add_argument('--rpi_port', default='5555')
parser.add_argument('--connect', default='udp:127.0.0.1:14551')
args = parser.parse_args()

# aquire connection_string
connection_string = args.connect
if not connection_string:
    sys.exit('Please specify connection string')

# Connect to the Vehicle
print('Connecting to vehicle on: %s' % connection_string)
copter = Copter(connection_string)
print("CONNECTED")

# Set up IP addresses and port
SERVER_IP = '192.168.1.164'  # replace with the IP address of the server
CLIENT_IP = '192.168.1.224'
PORTpi = 6001 # replace with any available port number
PORTgcs = 5501

# Create socket object
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # DGRAM MAKES IT UDP
s.bind((SERVER_IP, PORTpi))

def get_location_metres(original_location, dNorth, dEast, altitude):
        """
        Returns a Location object containing the latitude/longitude `dNorth` and `dEast` metres from the
        specified `original_location`. The returned Location has the same `alt and `is_relative` values
        as `original_location`.
        The function is useful when you want to move the vehicle around specifying locations relative to
        the current vehicle position.
        The algorithm is relatively accurate over small distances (10m within 1km) except close to the poles.
        For more information see:
        http://gis.stackexchange.com/questions/2951/algorithm-for-offsetting-a-latitude-longitude-by-some-amount-of-meters
        """
        earth_radius=6378137.0 #Radius of "spherical" earth
        #Coordinate offsets in radians
        dLat = dNorth/earth_radius
        dLon = dEast/(earth_radius*math.cos(math.pi*original_location.lat/180))

        #New position in decimal degrees
        newlat = original_location.lat + (dLat * 180/math.pi)
        newlon = original_location.lon + (dLon * 180/math.pi)
        
        return LocationGlobalRelative(newlat, newlon,altitude)


# setup listeners to get all messages from the copter
copter._setup_listeners()

# give some time for all changes to take place
time.sleep(2)

# print current coordinates to check for good GPS signal
print("Bypass Here - FOR DEBUG ONLY🫡")

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
pic_count = 0

#Reusable take picture+save image function
def take_picture(pic_count):
    print("Taking picture in 3 seconds!")
    time.sleep(3)
    ret, image=cam.read() #Live view of camera frame
    print("Taking picture now!")
    time.sleep(1)
    imagefilename = os.path.join(cwd, f'test_{pic_count}.jpg')
    cv2.imwrite(imagefilename, image)  # Save picture to the rpi
    Tarps = Check_Picture_Find_Coords(imagefilename, copter.pos_alt_rel, (copter.pos_lon,copter.pos_lat), pic_count)

    if Tarps is not None: #This loop executed if tarp is found
        imagefilename = os.path.join(cwd, f'test_{pic_count}_marked.jpg')
        cv2.imwrite(imagefilename, image)  # Save picture to the rpi
        packet = {
                    "target_x" : Tarps[0],
                    "target_y" : Tarps[1]
                  }   
        # convert to bytes for socket data transfer
        packet_bytes = json.dumps(packet).encode('utf-8')
        # send data to the GCS
        s.sendto(packet_bytes, (CLIENT_IP, PORTgcs))

def dummy_take_picture(pic_count):
    """
    This function can be used to run this file in SITL without errors because SITL may not
    be configured to take pictures and will throw errors. 
    """
    print(pic_count)

def tarp_centering():
    """"
    This function implements tarp centering after the tarp has been located in order to 
    increase accuracy when dropping payload. 
    """
    lower_blue = np.array([0, 80, 0])  # Lower bound of the blue color range in HSV
    upper_blue = np.array([255, 250, 45])  # Upper bound of the blue color range in HSV
    pic_count = 0
    #centered = False
    #while not (centered):
    # Read the image from the drone's camera
    ret, image=cam.read()
    #IMPLEMENT CAMERA CAPTURE HERE
    cwd = os.getcwd()
    imagefilename = os.path.join(cwd, f'centering_image_{pic_count}.jpg')
    cv2.imwrite(imagefilename, image)  # Save picture to the rpi

    image = cv2.imread(imagefilename)
    pic_count+=1
    # Get the center of the tarp using the detect_blue_cluster() function
    tarp_center = detect_blue_cluster(image, lower_blue, upper_blue)

    # Define the image center
    image_center = (image.shape[1] // 2, image.shape[0] // 2)

    # Calculate the pixel difference between the image center and the tarp center
    dx = tarp_center[0] - image_center[0]
    dy = tarp_center[1] - image_center[1]

    # Check if the tarp is centered within 5% of the image dimensions
    if abs(dx) < 0.05 * image.shape[0] and abs(dy) < 0.05 * image.shape[1]:
        centered = True
        print("Tarp centered")
        #continue

    # As in the Check Image Get Coords function Here is the calculated values for each pixel in meters
    PixelMetersWidth  = 0.0341
    PixelMetersHeight = 0.0455

    # The below sets the difference in meters by 1/10 of the pixel differences
    incremental_distance_x =  dx * PixelMetersWidth
    incremental_distance_y =  dy * PixelMetersHeight


    # Update the current location
    currentLocation = copter.vehicle.location.global_relative_frame

    # Update the target location based on the calculated incremental distances
    targetLocation = get_location_metres(currentLocation, incremental_distance_y, incremental_distance_x, 50)

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
    take_picture(pic_count)
    pic_count=pic_count+1 


print("debug 🫡")


print("Waiting for GCS")
msg = s.recvfrom(4096)
        
print(msg)
data = msg[0]
print (data)
gcsCmd = json.loads(data.decode('utf-8'))
print("Command Received")
print(data)

# create location object from GCS calculated coordinate
targetCoordinate = LocationGlobalRelative(gcsCmd[0], gcsCmd[1], 50) # drops altitude to 40 to center over target
# go to calculated coordinate
copter.vehicle.simple_goto(targetCoordinate)
print("Going to click")

while(copter.distance_to_current_waypoint(gcsCmd[0], gcsCmd[1], 50) > float(position_buffer)):
        time.sleep(1)
        print(copter.distance_to_current_waypoint(gcsCmd[0], gcsCmd[1], takeoff_alt), float(position_buffer))
#print("GOING TO TARGET and sleeping for 15")
print("Sleeping for 2 seconds before starting centering.")
time.sleep(2)

#tarp centering not implemented in final demo, but is included below for reference 
#tarp_centering()
# targetCoordinate = LocationGlobal((copter.pos_lon,copter.pos_lat, 50)) # Updates targ coord to where it centered at 40m
# copter.vehicle.simple_goto(targetCoordinate)
#while(copter.distance_to_current_waypoint(gcsCmd[0], gcsCmd[1], 50) > float(position_buffer)):
        #time.sleep(1)
        #print(copter.distance_to_current_waypoint(gcsCmd[0], gcsCmd[1], takeoff_alt), float(position_buffer))
#tarp_centering() # centers again at 20M

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
