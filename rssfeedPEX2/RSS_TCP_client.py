"""
    # RSS_TCP_client.py

    Author: Brian Yarbrough, November 2015
        Adopted from Dr. Brown TCP Demo Code

    Fetches RSS feeds and allows user to open articles
    PEX2, CS 467


"""
import sys, socket
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import os, webbrowser

# ---------------------------------------------------------------------


def main():

    # get URL from command line
    url = ""
    if len(sys.argv) == 2:
        try:
            url = sys.argv[1]
        except TypeError:
            print("Argument: Invalid URL")
    else:
        raise SyntaxError("Server only excepts one argument <URL>")

    print("\nWelcome to Brian's RSS Browser\n\nSelect articles to open\nUse 'h' for help\n")

    rss_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    rss_socket.settimeout(5.0)
    rss_raw = ""
    try:
        # TCP connection
        (rss_socket, path, netloc) = new_retriever(url)
        # get the feed
        print('getting feed')
        rss_raw = receive_content(rss_socket, path, netloc)
    except socket.timeout:
        print("Did not receive response from server; server possibly down.")
    except ConnectionResetError:
        print("Error: connection to server reset")
    except:
        print("Unexpected error: ", sys.exc_info()[0])
    finally:
        # close socket and free up memory
        rss_socket.close()
        del rss_socket

    # parse the xml
    rss_pretty = parseXML(rss_raw)
    # interact with user until exit
    prompt(rss_pretty)


def receive_content(my_socket, path, netloc):
    print('Communicating...')
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
        total_response += h_response.decode('UTF-8', 'ignore')

    # content length transfer
    if 'Content-Length' in total_response:
        print('Getting based on Content-Length')
        # get expected length from HTTP header
        index_content_length = total_response.index('Content-Length')
        nums = [int(s) for s in total_response[index_content_length:].split() if s.isdigit()]
        content_length = nums[0]
        # content length minus what has already been received and header
        head_end = total_response.index('\r\n\r\n')
        total_response = total_response[head_end:]
        amount_expected = content_length - (1020-head_end)
        amount_received = 0

        # get up to that length
        while amount_received < amount_expected:
            response = my_socket.recv(buffer_size)
            amount_received += len(response)
            # build response from multiple packets
            total_response += response.decode('UTF-8', 'ignore')

        return total_response
    # receive chunked transfer
    # note, this does not always work - rerun and it usually will
    elif 'Transfer-Encoding: chunked' in total_response:
        print('Getting based on Chunked Transfer')
        head_end = total_response.index('\r\n\r\n')
        total_response = total_response[head_end+4:]
        # chunk length is hex number at start of chunk
        next_length = int(total_response[:total_response.index('\n')], 16)
        amount_received = len(total_response[total_response.index('\n'):])

        # continue fetching
        while next_length != 0:
            response = ""
            while amount_received < next_length+4:
                response = my_socket.recv(buffer_size)
                amount_received += len(response)
                # build response from multiple packets
                total_response += response.decode('UTF-8', 'ignore')
            # account for part of this chunk already gotten
            amount_received -= (next_length+4)
            # get length of next chunk
            r_split = response.decode('UTF-8', 'ignore').splitlines()
            for line in reversed(r_split):
                if line != '' and '<' not in line and '>' not in line:
                    next_length = int(line, 16)
                    break

        return total_response

    else:
        raise ValueError('Transfer protocol not supported')


def prompt(rss):
    # prompt user
    choice = 'display'
    while choice != 'q':
        if choice == 'display':
            # display the articles
            for i in range(0,len(rss)):
                print(i,rss[i])
        elif choice == 'h':
            # help menu
            print("Help Menu")
            print('display : show article choices ')
            print('q : exit')
            print('enter an article number to open it')
        elif choice.isdigit():
            if int(choice) < len(rss):
                open_article(rss[int(choice)])
            else:
                print('No such article in this feed')
        # prompt user
        choice = input('\nEnter article number you wish to open: ').lower()
    # program exit
    print('Goodbye!')


def open_article(rss):
    # get article  from server
    print('Opening',rss[0])
    article_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    article_socket.settimeout(5.0)
    try:
        (article_socket, path, netloc) = new_retriever(rss[1])
        web_page = receive_content(article_socket, path, netloc)
    except socket.timeout:
        print("Did not receive response from server; server possibly down.")
    except ConnectionResetError:
        print("Error: connection to server reset")
    except:
        print("Unexpected error: ", sys.exc_info()[0])
    finally:
        # close socket and free up memory
        article_socket.close()
        del article_socket

    # Save the web page to a file
    filename = os.path.dirname(__file__) + "/temp.html"
    print("Saving web page to ... -->", filename)
    with open(filename, 'w') as f:
        f.write(web_page)
    # Open the file in the default web browser
    print("Opening the web page in a browser")
    webbrowser.open('file://' + filename)


def new_retriever(url):
    # parse URL
    (scheme,netloc,path,params,query,fragment) = urlparse(url)
    # check if valid
    if netloc == "" or path == "":
        raise SyntaxError('Invalid URL: "' + url + '"')
        exit()
    # Open TCP to IP address
    server_addr = socket.gethostbyname(netloc)
    server_port = 80
    print('Opening socket to',server_addr,'on port',server_port)
    # new TCP socket on random port
    new_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    new_socket.settimeout(5.0)
    # TCP connection
    new_socket.connect((server_addr, server_port))

    return new_socket, path, netloc


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

