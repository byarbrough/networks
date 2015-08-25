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
import queue

# ----------------Network socket setup------------------------
# Create a socket: IPv4 protocol and sends UDP datagrams
s_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Assign socket arbitrary port greater than 1023
server_port = 1055
s_socket.bind(('', server_port))

# Max message size
buffer_size = 4096
# -------------------------------------------------------------

# --------------define functions-------------------------------
answer = ['g', 'g', 'g', 'g']
nGuess = 1
global history

## function to start a new game
def newGame():
    global nGuess

    letters = ['A', 'B', 'C', 'D', 'E', 'F']
    # randomly generate an answer
    for c in range(4):
        answer[c] = random.choice(letters)
    nGuess = 1

    print("answer is ", answer)

def replyM(m):
    m = m.upper()
    s_socket.sendto(m.encode('utf-8'), cAddress)

def handleGuess(g):
    global nGuess

    parted = g.partition(',') # Split into array
    guess = parted[2].strip() # Remove whitespace and store guess
    # Check for errors in guess
    if len(guess) != 4:
        replyM('ERROR_REPLY, BAD LENGTH')
        return
    nCorrect = 0
    for i in range(4):
        if answer[i] == guess[i]:
            nCorrect += 1
    #history[nGuess*2] = g  # store the guess
    #history[nGuess*2+1] = nCorrect  # store the number correct

    # Check for wins/ losses, reply to user
    if nCorrect == 4:
        replyM('YOU WIN!')
    elif nGuess == 10:
        replyM('GAME OVER')
    else:
        replyM('GUESS_REPLY '+ 'guess # ' + str(nGuess) + ': ' + str(nCorrect) + ' letters correct')
        nGuess += 1


def handleHistory():
    reply = 'HISTORY_REPLY' + str(history)
    replyM(reply)



# first initialization
newGame()

## Main infinite loop ##
while True:

    # Wait for messsage from client
    (cData, cAddress) = s_socket.recvfrom(buffer_size)
    cData = cData.decode()
    print("Message: ", cData)
    print("Client address: ", cAddress)
    # Handle client message
    if cData == 'RESET':
        replyM('RESET_REPLY')
        newGame()
    elif cData == 'HISTORY':
        replyM('HISTORY_REPLY')
    elif cData.startswith('GUESS,'):
        handleGuess(cData)
    else:
        replyM('ERROR_REPLY')


# END LOOP

# After infinite loop. Never called
s_socket.close()
del s_socket