#!/usr/bin/python3
#
# Wesleyan University
# COMP 332, Spring 2018
# Homework 3: Simple multi-threaded web proxy

# Usage:
#   python3 web_proxy.py <proxy_host> <proxy_port> <requested_url>
#
# Nikhil Ghosh

# Python modules
import socket
import sys
import threading

# Project modules
import http_constants as const
import http_util


class WebProxy():

    def __init__(self, proxy_host, proxy_port):
        self.proxy_host = proxy_host
        self.proxy_port = proxy_port
        self.proxy_backlog = 1
        self.proxy_cache = {}
        self.start()

    def start(self):

        # Initialize server socket on which to listen for connections
        try:
            proxy_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            proxy_sock.bind((self.proxy_host, self.proxy_port))
            proxy_sock.listen(self.proxy_backlog)
        except OSError as e:
            print ("Unable to open proxy socket: ", e)
            if proxy_sock:
                proxy_sock.close()
            sys.exit(1)

        # Wait for client connection
        while True:
            conn, addr = proxy_sock.accept()
            print ('Client has connected', addr)
            thread = threading.Thread(target = self.serve_content, args = (conn, addr))
            thread.start()

    def serve_content(self, conn, addr):

        # Receive binary request from client
        bin_req = conn.recv(4096)
        try:
            str_req = bin_req.decode('utf-8')
            print(str_req)
        except ValueError as e:
            print ("Unable to decode request, not utf-8", e)
            conn.close()
            return

        # Extract host and path
        hostname = http_util.get_http_field(str_req, 'Host: ', const.END_LINE)
        pathname = http_util.get_http_field(str_req, 'GET ', ' HTTP/1.1')
        if hostname == -1 or pathname == -1:
            print ("Cannot determine host")
            client_conn.close()
            return
        elif pathname[0] != '/':
            [hostname, pathname] = http_util.parse_url(pathname)
        str_req = http_util.create_http_req(hostname, pathname)
        url = hostname + pathname

        # add to cache if not present, append cached date to modify request if applicable
        if url in self.proxy_cache:
            print('********************** URL in the cache already... ********************** ')
            [temp_response, temp_date] = self.proxy_cache[url]
            print("Printing cached response: ", temp_response)
            print("Printing cached date: ", temp_date)
            new_string_req = http_util.add_http_field(str_req, "If-Modified-Since", str(temp_date))
            print('********************** String request updated:******************* ')
            print(new_string_req)
            str_req = new_string_req
            bin_req = str_req.encode('utf-8')

        # Open connection to host and send binary request
        try:
            web_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            web_sock.connect((hostname, 80))
            print ("********************** Sending request to web server ********************** ")
            print ("Request: ", str_req)
            web_sock.sendall(bin_req)
        except OSError as e:
            print ("Unable to open web socket: ", e)
            if web_sock:
                web_sock.close()
            conn.close()
            return

        # Wait for response from web server
        bin_reply = b''
        while True:
            more = web_sock.recv(4096)
            if not more:
                 break
            bin_reply += more
        
        # Find the date element from the response
        print('********************** Decoding and date extraction ********************** ')
        try:
            response = bin_reply.decode('utf-8')
            try:
                date = http_util.get_http_field(response, "Last-Modified: ", const.END_LINE)
                print(date)
            except:
                date = http_util.get_http_field(response, "Date: ", const.END_LINE)
                print(date)
        except ValueError as e:
            print("ERROR: Unable to decode URL object: ", e)

        # isolate response code
        code = http_util.get_http_field(response, "HTTP/1.1 ", const.END_LINE)
        print('********************** HTTP Code extraction ********************** ')
        print('Code: ', code)

        # Implement caching
        if code == "304 Not Modified":
            # send encoded cached response
            reply = self.proxy_cache[url][0].encode('utf-8') # format in dict: cache[url] = [response, date]
            print('********************** Response received, no modifications... ********************** ')
            print('Cached response: ', reply[:300])
            conn.sendall(reply)
            print('Came from the cache!')
            # Close connection to client
            conn.close()
        elif code == "200 OK": # when it HAS been modified
            # update cache
            self.proxy_cache[url] = [response, date]
            reply = response
            print('********************** Response received from server... ********************** ')
            print('Cache updated, showing 1st 300 bytes...')
            print('Response: ', reply[:300])
            conn.sendall(bin_reply)
            print('Came from updated response!')
            # Close connection to client
            conn.close()
        else: # Some error with the response code or request
            print("Problem with request... closing connection")
            conn.close()

def main():

    print (sys.argv, len(sys.argv))

    proxy_host = 'localhost'
    proxy_port = 50007

    if len(sys.argv) > 1:
        proxy_host = sys.argv[1]
        proxy_port = int(sys.argv[2])

    web_proxy = WebProxy(proxy_host, proxy_port)

if __name__ == '__main__':

    main()
