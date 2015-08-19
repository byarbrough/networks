# MastermindClient.py
#
# Author: Brian Yarbrough
# PEX1, CS 467, USAFA
# August 2015
#
# Based on UDPClient by Wayne Brown

"""
    The client for playing the game. It runs for a short time.
    The client must know the host name and process port number that
    it wants to communicate with. Notice that these values match the server program.
"""

# The socket library allows for the creation and use of the TCP and UDP protocols.
# See https://docs.python.org/3/library/socket.html
import socket

# Create a new socket on random port
c_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Send a request to the server.
server_name = '127.0.0.1' # localhost
server_port = 1055 #same machine

## function for sending message to server
def sendM(m):
    m = m.upper()
    c_socket.sendto(m, (server_name, server_port))
    print(m)

sendM(b'reset')

# c_socket.sendto(message, (server_name, server_port))


# Wait for the response from the server; max buffer size
buffer_size = 4096
(response, server_address) = c_socket.recvfrom(buffer_size)

#print response from server
print("Server response: ", response)
print("Server address:  ", server_address)

# Close the socket and delete from memory
c_socket.close()
del c_socket

