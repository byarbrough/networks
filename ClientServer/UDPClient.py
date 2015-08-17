# UDPCLient.py
#
# Author: Wayne Brown, August 2015

"""
    A demonstration of a typical client using the UDP protocol. A client typically runs
    for a short time. The client must know the host name and process port number that
    it wants to communicate with. Notice that these values match the server program.
"""

# The socket library allows for the creation and use of the TCP and UDP protocols.
# See https://docs.python.org/3/library/socket.html
import socket

# Create a new socket to communicate with a remote server
#   AF_INET means we want an IPv4 protocol
#   SOCK_DGRAM means we want to send UDP datagrams
# The socket is assigned a random port number. Clients typically have random port numbers.
my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Send a request to the server.
# The first parameter is a byte array. The prefix b' makes the string a byte array
# instead of a unicode string.
# The second parameter is the address of the server as a tuple: (address, port_number)
server_name = '127.0.0.1' # localhost
server_port = 1055
message = b'request'
my_socket.sendto(message, (server_name, server_port))

# Wait for the response from the server - this blocks until the server responds.
# The parameter is the maximum size of the receive buffer, in bytes.
buffer_size = 4096
(response, server_address) = my_socket.recvfrom(buffer_size)
print("Server response: ", response)
print("Server address:  ", server_address)

# Close the socket, which releases all of the memory resources the socket used.
my_socket.close()

# Delete the socket from memory to again reclaim memory resources.
del my_socket