import socket

# Set up IP address and port
SERVER_IP = '127.0.0.1'  # replace with the IP address of the server
PORT = 5500  # replace with the port number used by the server

# Create socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Set socket timeout to 1 second
s.settimeout(1)

# Attempt to connect to server
try:
    s.connect((SERVER_IP, PORT))
    print('Server is running and listening on', SERVER_IP, 'port', PORT)
except socket.error:
    print('Server is not running or not listening on', SERVER_IP, 'port', PORT)

# Close socket connection
s.close()
