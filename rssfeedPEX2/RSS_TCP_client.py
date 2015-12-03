"""
    # RSS_TCP_client.py

    Author: Brian Yarbrough, November 2015
        Adopted from Dr. Brown TCP Demo Code


"""
import sys, socket
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import os, webbrowser

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

    rss_raw = ""
    try:
        # TCP connection
        my_socket.connect((server_addr, server_port))

        # get the feed
        rss_raw = receive_content_length(my_socket,path,netloc)

    except socket.timeout:
        print("Did not receive response from server; server possibly down.")
    except ConnectionResetError:
        print("Error: connection to server reset")
    except:
        print("Unexpected error: ", sys.exc_info()[0])
    finally:
        # close socket and free up memory
        my_socket.close()

    # parse the xml
    rss_pretty = parseXML(rss_raw)
    # display the articles
    for i in range(0,len(rss_pretty)):
        print(i,rss_pretty[i])
    # Delete the socket from memory
    del my_socket

def receive_content_length(my_socket,path,netloc):

    # The size of the TCP receive buffer
    buffer_size = 1024

    # request RSS feed from server
    message = "GET " + path + " HTTP/1.1\n" + "HOST: " + netloc + " \n\n"
    my_socket.sendall(message.encode('utf-8'))

    # counters
    amount_expected = 1024
    amount_received = 0
    total_response = ""
    # receive the first buffer worth
    while amount_received < amount_expected:
        h_response = my_socket.recv(buffer_size)
        amount_received += len(h_response)
        total_response += h_response.decode('utf8', 'replace')

    # get expected length from HTTP header
    try:
        index_content_length = total_response.index('Content-Length')
        nums = [int(s) for s in total_response[index_content_length:].split() if s.isdigit()]
        content_length = nums[0]
        # content length minus what has already been received and header
        head_end = total_response.index('\r\n\r\n')
        total_response = total_response[head_end:]
        amount_expected = content_length - (1020-head_end)
        amount_received = 0
    except ValueError:
        print('Content-Length absent from header')

    # get up to that length
    while amount_received < amount_expected:
        response = my_socket.recv(buffer_size)
        amount_received += len(response)
        # build response from multiple packets
        total_response += response.decode('utf8', 'replace')

    return total_response


def parseXML(text):
    """ Parse a HTML/XML data string that is a typical RSS feed into
        information about individual articles
    :param text: A HTML/XML data string
    :return: A list of articles. Each article is a (title, link) tuple
    """
    soup = BeautifulSoup(text, "html.parser")
    articles = []
    for oneItem in soup.findAll('item'):
        title = oneItem.find('title').text
        link = oneItem.find('link').text

        articles.append((title, link))

    return articles


# ---------------------------------------------------------------------
if __name__ == '__main__':
    main()
# ---------------------------------------------------------------------

