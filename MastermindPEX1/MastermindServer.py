# MastermindServer.py
#
# Author: Brian Yarbrough
# PEX1, CS 467, USAFA
# September 2015
# Version 1.1
# Based on UDPServer by Wayne Brown

"""
    Server for Mastermind, communicates with MastermindClient.py
    Runs continuously on infinite loop
    Follows RFC Protocol outlined by Dr. Brown
"""

# The socket library allows for the creation and use of the TCP and UDP protocols.
# See https://docs.python.org/3/library/socket.html
import socket
import random
import sys

# Create a socket: IPv4 protocol and sends UDP datagrams
s_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_port = 12345
if len(sys.argv) == 2 :
    try:
        server_port = int(sys.argv[1])
    except TypeError:
        print("Argument: Port must be an integer")
elif len(sys.argv) > 2:
    raise SyntaxError("Server only excepts one argument <port>")

s_socket.bind(('', server_port))

# Max message size
buffer_size = 4096

answer = ['g', 'g', 'g', 'g']
nGuess = 10
record = []


# function to start a new game
def newGame():
    global nGuess
    global record
    print('\r\nNEW GAME')
    letters = ['A', 'B', 'C', 'D', 'E', 'F']
    # randomly generate an answer
    for c in range(4):
        answer[c] = random.choice(letters)
    nGuess = 10
    record = []
    print("answer is ", answer)

def replyM(m):
    m = m.upper()
    print('Response: ' + m)
    try:
        s_socket.sendto(m.encode('utf-8'), cAddress)
    except:
        print("Error communicating with client")

def handleGuess(g):
    global nGuess

    parted = g.partition(',')  # Split into array
    guess = parted[2].strip()  # Remove whitespace and store guess
    # Check for bad length
    if len(guess) != 4:
        replyM('ERROR_REPLY, ' + '"' + g + '"')
        return

    nCorrect = 0
    # Traverse answer
    for i in range(4):
        # Check for invalid characters
        if guess[i] not in ['A', 'B', 'C', 'D', 'E', 'F']:
            replyM('ERROR_REPLY, ' + '"' + g + '"')
            return
        # Count correct letter
        elif answer[i] == guess[i]:
            nCorrect += 1

    # Store the guess
    record.append(guess)
    record.append(nCorrect)
    # Check for wins/ losses, reply to user
    if nCorrect == 4: # Win
        ans = ''
        for i in range(4):
            ans += answer[i]
        replyM('FEEDBACK_REPLY, ' + str(nCorrect) + ', ' + str(nGuess))
        print('Client Win')
        replyM('RESET_REPLY, ' + str(ans) + ', ' + str(nGuess))
        newGame()
    else: # Incorrect answer
        nGuess -= 1
        if nGuess <= 0: # Loss
            ans = ''
            for i in range(4):
                ans += answer[i]
            replyM('FEEDBACK_REPLY, ' + str(nCorrect) + ', ' + str(nGuess))
            print('Client Loss')
            s_socket.recvfrom(buffer_size)
            replyM('RESET_REPLY, ' + str(ans) + ', ' + str(nGuess))
            newGame()
        else: # Keep guessing
            replyM('FEEDBACK_REPLY, ' + str(nCorrect) + ', ' + str(nGuess))


# first initialization
newGame()

# Main infinite loop
while True:

    # Wait for message from client
    (cData, cAddress) = s_socket.recvfrom(buffer_size)
    cData = cData.decode().upper()

    print("Message: ", cData)
    print("Client address: ", cAddress)
    # Handle client message
    if cData == 'RESET':
        ans = ''
        for i in range(4):
            ans += answer[i]
        replyM('RESET_REPLY, ' + str(ans) + ', ' + str(nGuess))
        newGame()
    elif cData == 'HISTORY':
        if len(record) == 0:
            replyM('HISTORY_REPLY,')
        else:
            reply = 'HISTORY_REPLY,' + str(record).strip('[]')
            replyM(reply)
    elif cData.startswith('GUESS,'):
        handleGuess(cData)
    else:
        replyM('ERROR_REPLY, ' + '"' + str(cData) + '"')
# END LOOP

# After infinite loop... only here as a matter of principle
s_socket.close()
del s_socket
