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
import sys

# ----------------Network socket setup------------------------
# Create a socket: IPv4 protocol and sends UDP datagrams
s_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_port = 12345
if len(sys.argv) == 2:
    try:
        server_port = int(sys.argv[1])
    except TypeError:
        print("Argument: Port must be an integer")
elif len(sys.argv) > 2:
    raise SyntaxError("Server only excepts one argument <port>")

s_socket.bind(('', server_port))

# Max message size
buffer_size = 4096
# -------------------------------------------------------------

# --------------define functions-------------------------------
answer = ['g', 'g', 'g', 'g']
nGuess = 10
global history


# function to start a new game
def newGame():
    global nGuess

    letters = ['A', 'B', 'C', 'D', 'E', 'F']
    # randomly generate an answer
    for c in range(4):
        answer[c] = random.choice(letters)
    nGuess = 10

    print("answer is ", answer)


def replyM(m):
    m = m.upper()
    s_socket.sendto(m.encode('utf-8'), cAddress)


def handleGuess(g):
    global nGuess

    parted = g.partition(',')  # Split into array
    guess = parted[2].strip()  # Remove whitespace and store guess
    # Check for bad length
    if len(guess) != 4:
        replyM('ERROR_REPLY, ' + g)
        return

    nCorrect = 0
    # Traverse answer
    for i in range(4):
        # Check for invalid characters
        if answer[i] not in ['A', 'B', 'C', 'D', 'E', 'F']:
            replyM('ERROR_REPLY, ' + g)
            return
        # Count correct letter
        elif answer[i] == guess[i]:
            nCorrect += 1

    # history[nGuess*2] = g  # store the guess
    # history[nGuess*2+1] = nCorrect  # store the number correct

    # Check for wins/ losses, reply to user
    if nCorrect == 4:
        replyM('YOU WIN!')
    else:
        nGuess -= 1
        if nGuess <= 0:
            replyM("GAME OVER, please reset")
        else:
            replyM('FEEDBACK_REPLY, ' + str(nCorrect) + ', ' + str(nGuess))



def handleHistory():
    reply = 'HISTORY_REPLY' + str(history)
    replyM(reply)


# first initialization
newGame()

# Main infinite loop
while True:

    # Wait for message from client
    (cData, cAddress) = s_socket.recvfrom(buffer_size)
    cData = cData.decode()

    print("Message: ", cData)
    print("Client address: ", cAddress)
    # Handle client message
    if cData == 'RESET':
        replyM('RESET_REPLY, ' + str(answer) + ', ' + str(nGuess))
        newGame()
    elif cData == 'HISTORY':
        replyM('HISTORY_REPLY')
    elif cData.startswith('GUESS,'):
        handleGuess(cData)
    else:
        replyM('ERROR_REPLY, ' + str(cData))


# END LOOP

# After infinite loop. Never called
s_socket.close()
del s_socket
