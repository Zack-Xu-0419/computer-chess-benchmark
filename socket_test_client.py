import socket

# Create a socket object
client_socket = socket.socket()

# Define host and port
host = '100.115.28.85'
port = 12345

# Connect to the server
client_socket.connect((host, port))

# Send a message
client_socket.send(b'Hello, server!')

# Close the socket
client_socket.close()
