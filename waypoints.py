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

# parse arguemnts from command line
parser = argparse.ArgumentParser()
parser.add_argument('--gcs_ip', default='192.168.1.148')
parser.add_argument('--gcs_port', default='4444')
parser.add_argument('--rpi_ip', default='192.168.1.147')
parser.add_argument('--rpi_port', default='5555')
parser.add_argument('--connect', default='udp:127.0.0.1:10000')
args = parser.parse_args()

# connect to copter on localhost
connection_string = args.connect
copter = Copter(connection_string)
print("CONNECTED")

# set up socket to send data to GCS
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
gcs_ip = args.gcs_ip
gcs_port = int(args.gcs_port)
rpi_port = int(args.rpi_port)
rpi_ip = args.rpi_ip
s.bind((rpi_ip, int(rpi_port)))


# setup listeners to get all messages from the copter
copter._setup_listeners()

# give some time for all changes to take place
time.sleep(2)

# print current coordinates to check for good GPS signal
print("LAT : " + str(copter.pos_lat))
print("LON : " + str(copter .pos_lon))

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

# 5m buffer for gps coordinates
position_buffer = 5

# print mission items for verification
print("MISSION LIST: \n" + str(missionlist))

# set copter to guided autopilot mode
copter.set_ap_mode("GUIDED")

print("Taking off")

# setting takeoff altitude m
takeoff_alt = 50

# take off to target altitude
copter.vehicle.simple_takeoff(takeoff_alt)

# wait while copter reaches desired altitude
while copter.pos_alt_rel < takeoff_alt:
    print("Gaining altitude")
    time.sleep(1)

time.sleep(5)

copter.vehicle.airspeed = 3 #m/s

# parse through each waypoint in file
for command in missionlist:
    # go to waypoint
    point1 = LocationGlobalRelative(command.x, command.y, command.z)
    copter.vehicle.simple_goto(point1)
    print("GOING TO NEXT WAYPOINT")
    time.sleep(5)

copter.set_ap_mode("RTL")