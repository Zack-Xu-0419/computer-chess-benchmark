import socket

# Create a socket object
server_socket = socket.socket()

# Define host and port
host = 'localhost'
port = 12345

# Bind to the port
server_socket.bind((host, port))

# Wait for client connection
server_socket.listen(5)

print("Server listening...")

# Establish connection with client
client_socket, addr = server_socket.accept()

print('Got connection from', addr)

# Receive data from the client
data = client_socket.recv(1024).decode()

print('Received:', data)

# Close the connection
client_socket.close()
