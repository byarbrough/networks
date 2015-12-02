"""
    # RSS_TCP_client.py

    Author: Brian Yarbrough, November 2015
        Adopted from Dr. Brown TCP Demo Code


"""
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
    server_addr = socket.gethostbyname(netloc)
    server_port = 80
    print('Fetching RSS from {} on port {}'.format(server_addr, server_port))
    my_socket.connect((server_addr, server_port))

    # The size of the TCP receive buffer
    buffer_size = 1024

    try:
        # request RSS feed from server
        message = "GET " + path + " HTTP/1.1\n" + "HOST: " + netloc + " \n\n"
        my_socket.sendall(message.encode('utf-8'))

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
