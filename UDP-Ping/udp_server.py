#######################################
# Nikhil Ghosh
# COMP 332: Networks
# Homework 6
#######################################

import socketserver
from socket import *
import random
import sys

class UDPServer:

    def __init__(self, udp_port):
        self.udp_port = udp_port
        self.start()

    def start(self):
        # Create a UDP Socket 
        serverSock = socket(AF_INET, SOCK_DGRAM)
        # Bind socket
        serverSock.bind(('',self.udp_port))
        
        # Wait for a connection from UDP Client
        while True:
            # Once we receive a message from the client (connectionless b/c UDP)
            msg, addr = serverSock.recvfrom(1024)
            
            # Random dropping of packets in order to test the timeout functionality
            # Step 1. generate random number
            rand = random.randint(0,101)
            
            # Step 2. If the random number is divisble by 10, don't respond. Otherwise, respond.
            if rand % 10 == 0:
                continue
            else:
                serverSock.sendto(msg,addr)


def main():

    print (sys.argv, len(sys.argv))
    udp_port = 50007

    if len(sys.argv) > 1:
        udp_port = int(sys.argv[1])

    udpserver = UDPServer(udp_port)

if __name__ == '__main__':
    main()
