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

        total_response = ""
        response = ""

        # run until end of rss feed
        while '</rss>' not in response:
            # recieve from server
            response = my_socket.recv(buffer_size).decode('utf8', 'replace')
            # build response from multiple packets
            total_response += response

        print(total_response)

    finally:
        # Close the socket, which releases all of the memory resources the socket used.
        my_socket.close()

    # Delete the socket from memory to again reclaim memory resources.
    del my_socket

# ---------------------------------------------------------------------
if __name__ == '__main__':
    main()
