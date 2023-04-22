import socket
import time

# Set up IP address and port
LOCAL_IP = '127.0.0.1'  # replace with the IP address of the server
PORT = 5500  # replace with the port number used by the server

# Create socket object
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setblocking(0)

# Set socket timeout to 1 second
# s.settimeout(1)
s.bind((LOCAL_IP, PORT))

# Attempt to connect to server
while True:
    time.sleep(2)
    try:
        message, address = s.recvfrom(4096)
        print(message)
        print('Server is running and listening on', address, 'port', PORT)
    except socket.error:
        print('Server is not running or not listening at port', PORT)

# Close socket connection
# s.close()
