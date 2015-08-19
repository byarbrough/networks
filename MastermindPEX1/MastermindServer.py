# MastermindServer.py
#
# Author: Brian Yarbrough
# PEX1, CS 467, USAFA
# August 2015
#
# Based on UDPServer by Wayne Brown

"""
    A demonstration of a typical server using the UDP protocol. A server typically runs
    24/7 and ony terminates when it is killed by an administrator. Thus the infinite
    loop. The port number is arbitrary, but it should be greater than 1023. Ports 0-1023
    are the reserved, "well known" ports.
"""

# The socket library allows for the creation and use of the TCP and UDP protocols.
# See https://docs.python.org/3/library/socket.html
import socket
import random

# Create a socket: IPv4 protocol and sends UDP datagrams
s_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Assign socket arbitrary port greater than 1023
server_port = 1055
s_socket.bind(('', server_port))

# Max message size
buffer_size = 4096

answer = b'abcd'

def newGame():
    letters = b'abcdef'
    print(letters)
    for c in range(4):
        #answer[c] = random.choice(letters)
        print(answer)

newGame()

# Infinite loop
while (True):

    # Wait for messsage from client
    (cData, cAddress) = s_socket.recvfrom(buffer_size)
    print("Message: ", cData)
    print("Client address: ", cAddress)

    if cData == "reset":
       newGame()



# Reply to client
s_socket.sendto(b'server response', cAddress)

# After infinite loop. Never called
s_socket.close()
del s_socket


