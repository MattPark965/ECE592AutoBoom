import socket
import time

# Set up IP addresses and port
SERVER_IP = '127.0.0.1'  # replace with the IP address of the server
CLIENT_IP = '10.154.60.204'  # replace with the IP address of the client
PORT = 5500  # replace with any available port number

# Create socket object
s = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM) # DGRAM MAKES IT UDP

# Bind socket to client IP and port
s.bind((SERVER_IP, PORT))

# Connect to server IP and port
#s.connect((SERVER_IP, PORT))

# Send message to server
while True:
    message = 'Hello, server!'
    s.sendto(message.encode(), (CLIENT_IP, PORT))
    time.sleep(2) 
    

# Receive message from server
data = s.recv(1024)
print('Received from server:', data.decode())

# Close socket connection
#s.close()
