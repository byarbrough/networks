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
import sys

# Create a new socket on random port
c_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Send a request to the server.
server_name = '127.0.0.1'  # localhost
server_port = 12345  # same machine

if len(sys.argv) == 3:
    try:
        server_name = str(sys.argv[1])
        server_port = int(sys.argv[2])
    except TypeError:
        print("Argument: Port must be an integer")
elif len(sys.argv) == 2:
    raise  SyntaxError("Most specify both address and port or use defaults")
elif len(sys.argv) > 3:
    raise SyntaxError("Server only excepts two arguments <address> <port>")

buffer_size = 4096

# Handle Arguments


playing = True


# function for sending message to server
def sendM(m):
    m = m.upper()
    c_socket.sendto(m.encode('utf-8'), (server_name, server_port))
    # Wait for the response from the server; max buffer size
    (reply, server_address) = c_socket.recvfrom(buffer_size)
    return reply, server_address


# send initial request to server
sendM("reset")

print('\r\nWelcome to Mastermind!')

# Main loop for game
while playing:
    cmd = input('Enter Command: ').upper()
    if cmd == "?":
        print('help menu')
    elif cmd == 'QUIT':
        playing = False
    else:
        reply, address = sendM(cmd)
        reply = reply.decode()
        # Handle Replies from Server
        if reply.startswith('FEEDBACK_REPLY'):
            nums = reply.split(',')
            print(str(nums[1]) + ' letters correct, ' + str(nums[2]) + ' guesses remaining')
        else:
            print(reply)


# Close the socket and delete from memory
print("Goodbye")
c_socket.close()
del c_socket

# python myserver.py host port
