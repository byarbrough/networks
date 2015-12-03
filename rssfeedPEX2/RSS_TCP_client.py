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

        # couters
        amount_expected = 1024
        amount_received = 0
        total_response = ""
        # recieve the first buffer worth
        while amount_received < amount_expected:
            h_response = my_socket.recv(buffer_size)
            amount_received += len(h_response)
            print(h_response)
            total_response += h_response.decode('utf8', 'replace')

        # get expected length from HTTP header
        try:
            index_content_length = total_response.index('Content-Length')
            print('index_content_length',index_content_length)
            nums = [int(s) for s in total_response[index_content_length:].split() if s.isdigit()]
            content_length = nums[0]
            print('content_length',content_length)
            # content length minus what has already been received and header
            amount_expected = content_length - (1020-total_response.index('\r\n\r\n'))
            amount_received = 0
        except ValueError:
            print('Content-Length absent from header')

        print('expected',amount_expected)
        while amount_received < amount_expected:
            response = my_socket.recv(buffer_size)
            amount_received += len(response)
            # build response from multiple packets
            total_response += response.decode('utf8', 'replace')
            print('recv',amount_received)

        print("The total response from the server was:\n" + total_response)

    finally:
        # Close the socket, which releases all of the memory resources the socket used.
        my_socket.close()

    # Delete the socket from memory to again reclaim memory resources.
    del my_socket

# ---------------------------------------------------------------------
if __name__ == '__main__':
    main()
