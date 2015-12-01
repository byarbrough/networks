"""
    # RSS_TCP_client.py

    Author: Brian Yarbrough, November 2015
        Adopted from Dr. Brown TCP Demo Code


"""

# The socket library allows for the creation and use of the TCP and UDP protocols.
# See https://docs.python.org/3/library/socket.html
import socket
import sys
from urllib.parse import urlparse


# ---------------------------------------------------------------------
def main():

    # get URL from command line
    URL = ""
    if(len(sys.argv)==2):
        try:
            URL = sys.argv[1]
        except TypeError:
            print("Argument: Invalid URL")
    elif len(sys.argv) > 2:
        raise SyntaxError("Server only excepts one argument <URL>")

    # parse the URL
    (scheme,netloc,path,params,query,fragment) = urlparse(URL)

    # new TCP socket on random port
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Open TCP to IP address
    server_name = socket.gethostbyname(netloc)
    server_port = 80
    print('Fetching RSS from {} on port {}'.format(server_name, server_port))
    my_socket.connect((server_name, server_port))

    # The size of the TCP receive buffer
    buffer_size = 16

    try:
        # Send the server a message.
        # The first parameter is a byte array. The prefix b' makes the string a byte array. Note that
        # TCP might break the message into smaller packets before it sends the data to the server.
        message = b'GET '
        print('sending "' + str(message) + '" to the server.')
        my_socket.sendall(message)

        # Wait for the response from the server. Because the server might send the
        # response in multiple packets, we need to potentially call recv multiple times.
        # Note that recv function blocks until there is data in the TCP receive buffer.
        amount_received = 0

        # This is based on the fact that the server is going to echo the message back to the
        # client. In a more normal case, you would read the input buffer until you found a
        # special character that was recognized as the "end of message" character. OR,
        # the server would include in its response the size of the message that is coming.
        amount_expected = len(message)
        total_response = ""

        while amount_received < amount_expected:
            response = my_socket.recv(buffer_size)
            print("Server response: ", response)
            amount_received += len(response)
            # build response from multiple packets
            total_response += response.decode('utf8', 'replace')

        print("The total response from the server was:\n" + total_response)

    finally:
        # Close the socket, which releases all of the memory resources the socket used.
        my_socket.close()

    # Delete the socket from memory to again reclaim memory resources.
    del my_socket

# ---------------------------------------------------------------------
if __name__ == '__main__':
    main()
