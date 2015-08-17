# UDPServer.py
#
# Author: Wayne Brown, August 2015

"""
    A demonstration of a typical server using the UDP protocol. A server typically runs
    24/7 and ony terminates when it is killed by an administrator. Thus the infinite
    loop. The port number is arbitrary, but it should be greater than 1023. Ports 0-1023
    are the reserved, "well known" ports.
"""

# The socket library allows for the creation and use of the TCP and UDP protocols.
# See https://docs.python.org/3/library/socket.html
import socket

# Create a socket for communication.
# The first socket is the module name. The second socket is a function call.
#   AF_INET means we want an IPv4 protocol
#   SOCK_DGRAM means we want to send UDP datagrams
my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to listen on a particular port (0-65535).
# Use a number greater than 1023. Ports 0-1023 are the reserved, "well known" ports.
# The parameter is a address defined as a tuple (host, port)
server_port = 1055
my_socket.bind( ('', server_port) )

# Define the maximum size of message that will be accepted
buffer_size = 4096

# Run the server 24/7 (24 hours a day, 7 days a week)
while (True):

    # Wait for a client to send the server a message.
    # The parameter is the buffer size - the maximum number of bytes it can receive in one message
    # The return values are the data buffer and the client's address: (host, port)
    (data, client_address) = my_socket.recvfrom(buffer_size)
    print("Message: ", data)
    print("Client address: ", client_address)

    # Send a reply message to the client
    # The first parameter must be a byte array. The prefix b' makes it a byte
    # string (instead of a unicode string)
    my_socket.sendto(b'server response', client_address)

# If the above loop was not infinite, the socket's resources should be reclaimed
my_socket.close()
del my_socket