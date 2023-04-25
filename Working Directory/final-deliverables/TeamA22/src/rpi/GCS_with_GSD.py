'''
    ECE 592 Spring 2023 continued by
    Dom Barrera
    ECE 592 - Autonomous Bomber
    Ayush Luthra
    Alex Wheelis
    Kishan Joshi
    Harrison Tseng 
    
'''
# import necessary libraries
import socket, keyboard, time
import matplotlib.pyplot as plt
import json
import sys
import numpy as np
import pickle
import sys
print("Python executable path:", sys.executable)

# Set up IP address and port
SERVER_IP = '127.0.0.1' 
LOCAL_IP = '10.155.58.30'  # replace with the IP address of the server
#LOCAL_IP = '0.0.0.0'  # replace with the IP address of the server
PORTpi = 6000  # replace with the port number used by the server
PORTgcs = 5501
# Create socket object
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#s.setblocking(0)

# Set socket timeout to 1 second
# s.settimeout(1)
s.bind((LOCAL_IP, PORTgcs))

# # Attempt to connect to server
# while True:
#     time.sleep(2)
#     try:
#         message, address = s.recvfrom(4096)
#         print(message)
#         print('Server is running and listening on', address, 'port', PORT)
#     except socket.error:
#         print('Server is not running or not listening at port', PORT)

# # Set up a UDP Communication Protocol
# s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# # Set RPI ip address and port
# rpi_ip = "127.0.0.1"  # Update this to the Raspberry Pi's IP address
# rpi_port = 5555
# # IP Address is the device running the SERVER (Ground Control Station)
# ip = "10.154.60.204"  # Update this to the ground control station's IP address
# port = 4444

# # bind the server ports
# s.bind((ip, port))

# set constants from camera hardware
IMAGE_HEIGHT = 1080
IMAGE_WIDTH = 1920
# better source https://www.techtravels.org/modifying-logitech-c920/#:~:text=The%20sensor%20is%204.8mm,crop%20factor%20of%20around%207.2.
FOCAL_LENGTH =.00367 # google c920 focal length 3.67 mm
SENSOR_WIDTH=.0048
SENSOR_HEIGHT= .0036
# source for corrctions https://stackoverflow.com/questions/50544727/distance-to-object-webcam-c920hd-or-use-opencv-calibrate-py#:~:text=Focal%20Length%20(mm)%3A%203.67mm


# Server setup successful
print("Starting")

# Create the "Map" to view data
fig, ax = plt.subplots()

# Plots an image on the map under any data points.
img = plt.imread("MAP.png")

# Plot Labels
plt.title("GCS")
plt.xlabel("Latitude")
plt.ylabel("Longitude")

# Range of Coordinates of where we fly.
ax.axis([-78.702385, -78.691902, 35.725121, 35.729265]) #TODO VERIFY COORDINATES
ax.imshow(img, extent=(-78.702385, -78.691902, 35.725121, 35.729265)) #TODO VERIFY COORDINATES

# Temporarily Initialize Map
for i in range(100):
    plt.pause(0.01)

# Hold Data As Lists for X and Y
lonXCoords = []
latYCoords = []

# Store Click Events in these variables
clickX, clickY = '', ''
ip_port = ''

# Calculate the estimated GPS location of a blue object using 
# drone altitude, pitch, roll, yaw 
# a known GPS location of the drone when the picture was taken
# calculated pixel coordinates of the blue object from the center of the image
def get_lat_long_of_target(target_px_coor, drone_lat_long_coor, drone_alt, drone_azimuth):
    """
    Parameters
    ----------
    target_px_coor : list
        (x, y)
    drone_lat_long_coor : list
        (long, lat)
    drone_alt : int64
        altitude in meters
    drone_azimuth : list
        (pitch, roll, yaw)
        values in radians
    Returns
    -------
    target_lat_long_coor: list
    """

    # pull gps coordinates from the parameters
    drone_lat = drone_lat_long_coor[1]
    drone_lon = drone_lat_long_coor[0]

    east_west_const =  1/(111111*np.cos(38*np.pi/180))
    north_south_const = 1/111111 # deg/meters

    lat_lon_const = 1/111111 # deg/meters


    # pull pitch/roll/yaw from the parameters
    PITCH = drone_azimuth[0]
    ROLL = drone_azimuth[1]
    YAW = drone_azimuth[2]
    
    # removed roll and pitch correction due to use of a gimble.
    lat =  drone_lat
    lon =  drone_lon
    # make a correction for heading.
    # cos / sin adjustment for pixels based on yaw angle
    #-----------------------------------------


    GSD_height = (drone_alt * SENSOR_HEIGHT)/(FOCAL_LENGTH * IMAGE_HEIGHT)
    GSD_width = (drone_alt * SENSOR_WIDTH)/(FOCAL_LENGTH * IMAGE_WIDTH)

    object_x = GSD_width * target_px_coor[0]
    object_y = GSD_height * target_px_coor[1]

    #Earth’s radius, sphere
    R=6378137

    #offsets in meters
    dn = object_y
    de = object_x

    #Coordinate offsets in radians
    dLat = dn/R
    dLon = (de/R)*(np.cos(np.pi*lat/180))

    #OffsetPosition, decimal degrees
    latO = lat + dLat * 180/np.pi
    lonO = lon + dLon * 180/np.pi

    # return calculated coordinates
    return [lonO, latO]


# Onclick provided by MatPlotLib
# Returns coordinates of any point on the map clicked (in lon, lat format).
def onclick(event):
    # Must be declared global to be stored properly
    global clickX, clickY
    clickX = event.xdata
    clickY = event.ydata
    #Confirmation of Click:
    print("Click Entered")
    print(clickX, clickY)

# Make/Enable Click Events
fig.canvas.mpl_connect('button_press_event', onclick)

# Receive Message from PI (Drone)
def receive_message():
    # Set RECEIVING end of communication to be nonblocking. ABSOLUTELY NECESSARY.
    s.setblocking(0)

    # Try because if you do not receive a message, you will timeout.
    # Instead of timing out, we can keep retrying for a message.
    while True:
        # time.sleep(2)    
        # msg, address = s.recvfrom(4096)
        # print(msg)
        # print('Server is running and listening on', address, 'port', PORT)
        try:
            time.sleep(2)  
            msg = s.recvfrom(4096)
            # recvfrom is a UDP command, recv is a TCP command, takes in argument (Buffer Size).
            # msg = s.recvfrom(4096)
            data = msg[0]
            ip_port = msg[1]
            # Using json to decode data. USE THIS EXACT FORMAT WHEN RECEIVING DATA
            decode_message = json.loads(data.decode('utf-8'))

            # Currently type(decode_message) is a way of checking whether this is the data we want.
            # The type we are looking for is dictionary.
            # If the message is anything else, the message was NOT meant to be sent to the server.
            if type(decode_message) is dict:
                xy = [decode_message['target_x'], decode_message['target_y']]
                # Add to plot, "s" argument is the added point's size.
                ax.scatter(xy[0], xy[1], s = 5)
                plt.pause(0.01)
            else:
                # If the message was not intended for us, print the message type.
                print(type(decode_message))

        # Except and triple quotes MUST BE INCLUDED to maintain nonblocking code.
        except socket.error:
            '''print('Server is not running or not listening at port', PORTpi)'''


while True:

    # Receive Message Protocol
    receive_message()

    # Terminate GCS if 'q'
    if keyboard.is_pressed('q'):
        break

    if keyboard.is_pressed('c'):
        # If click inputs were previously received:
        if clickX and clickY:
            sendXlon = float(clickX)
            sendYlat = float(clickY)
            confirmCommand = input(f"You have selected {sendYlat}, {sendXlon} as your bombing location. Confirm bombing? (y/n)")

            # If INPUT for bombing 'y', send a list given [X, Y]
            if confirmCommand == 'y':
                print("SENDING COORDINATES")
                send_data = [sendYlat, sendXlon]
                packet = json.dumps(send_data).encode('utf-8')
                s.sendto(bytes(packet), (SERVER_IP, PORTpi)) # pi IP
                print("SENT COORDINATES")
                time.sleep(2)

    plt.pause(0.01)

# Extra Command that may be necessary / useful later
# plt.show()

# Extra Notes:
# Please note that heavy amounts of data further slows down the plotting, causing a delay.
# Consider using a time.sleep() or equivalent code on the CLIENT SIDE to help slow down data rates.

# When pressing 'q', 'c', 'a', from "keyboard.ispressed()", BE CAREFUL. PROGRAM IS HEAVILY KEYBOARD SENSITIVE.
# PRESSING OUTSIDE OF PROGRAM / COMMAND LINE WILL RUN THE COMMAND
# IMPORTANT NOTE: This is different from the "input()" command.
# Confirmation for bombing MUST BE DONE IN THROUGH THE COMMAND LINE PROMPT (When prompted.)

# You may have to press 'q', 'c', 'a', MULTIPLE TIMES in order for command to process through.
# This is because of the earlier note (slows down plotting and thus the script entirely).

# Currently sending GPS locations as a list [X,Y] or [longitude, latitude].
# You may want to double check whether X = lon and Y = lat (So I don't send the drone to Australia).
