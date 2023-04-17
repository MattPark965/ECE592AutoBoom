from pymavlink import mavutil

# Replace the serial_port variable with the actual serial port from step 5
serial_port = '/dev/serial/by-id/your_serial_port_here' # run "ls /dev/serial/by-id/"
baudrate = 57600

# Connect to the flight controller
mav = mavutil.mavlink_connection(serial_port, baud=baudrate)

def print_telemetry():
    while True:
        msg = mav.recv_match(blocking=True)
        if msg is not None:
            if msg.get_type() == "VFR_HUD":
                print("Altitude: {} m".format(msg.alt))
                print("Ground speed: {} m/s".format(msg.groundspeed))
                print("Airspeed: {} m/s".format(msg.airspeed))
                print("Heading: {} deg".format(msg.heading))
                print("Throttle: {} %".format(msg.throttle))
                print("Climb rate: {} m/s".format(msg.climb))
                print("---------------")

if __name__ == "__main__":
    print_telemetry()
