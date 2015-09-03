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

# function for sending message to server
def sendM(m):
    m = m.upper()
    c_socket.sendto(m.encode('utf-8'), (server_name, server_port))
    # Wait for the response from the server; max buffer size
    (reply, server_address) = c_socket.recvfrom(buffer_size)
    return reply, server_address

def printHelp():
    print("Mastermind Client, by Brian Yarbrough")
    print("All guesses must be four letters")
    print("Guesses may only contain the letters a-f")
    print("Enter 'history' to see your guesses")
    print("Enter 'reset' to start a new game")
    print("Enter 'quit' to leave the game")

def printHistory(h):
    n = int(len(h)/11)-1 # Number of guesses
    print('\tGuess\tNumber Correct')
    for i in range(1,n):
        shift = int(14 + (i-1)*11)
        print(shift)
        last = int(shift + 4)
        correct = int(i*11+11)
        print(last)
        print(correct)
        print(str(h[s]))
        #print('\t' + str(h[shift, last]) + '\t' + str(h[correct]))
    print(reply)
    print(len(reply))

def printReset(r):
    reply = r.split(',')
    ans = str(reply[1])
    ans += str(reply[2])
    ans += str(reply[3])
    ans += str(reply[4])
    answer = ''
    for i in range(18):
        if ans[i].isalpha():
            answer += ans[i]
    print("Previous answer: " + answer + " with " + str(reply[5]) + " guesses remaining.")
    print("New Game Started\r\n")


# Create a new socket on random port
c_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Send a request to the server.
server_name = '127.0.0.1'  # localhost
server_port = 12345  # same machine

# Handle Arguments
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

playing = True
print("\r\nWelcome to Mastermind!")

# send initial request to server
reply, addr = sendM('HISTORY')
print("Successful connection to " + str(addr[0]) + " on port " + str(addr[1]))
print("Current Server State: ")
print(reply.decode())
print("\r\nEnter a four letter guess or ? for help\r\n")

# Main loop for game
while playing:
    cmd = input("Enter a guess: ").upper()
    if cmd == "?":
        printHelp()
    elif cmd == 'QUIT':
        playing = False
    elif len(cmd) == 4: # Assume input is a guess
        cmd = "GUESS, " + cmd

    # Send message to server via sendM()
    reply = ''
    if cmd != '?':
        reply, address = sendM(cmd)
        reply = reply.decode()

    # Handle Replies from Server
    if reply.startswith('FEEDBACK_REPLY'):
        nums = reply.split(',')
        print(str(nums[1]) + " letters correct, " + str(nums[2]) + ' guesses remaining')
    elif reply.startswith('HISTORY_REPLY'):
        printHistory(reply)
    elif reply.startswith('RESET_REPLY'):
        printReset(reply)
    elif reply.startswith('ERROR_REPLY'):
        print("There was an error with your input: " + str(reply))
        print("Enter ? for help")
    else:
        print(reply)


# Close the socket and delete from memory
print('Goodbye')
c_socket.close()
del c_socket
