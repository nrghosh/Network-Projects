#######################################
# Nikhil Ghosh
# COMP 332: Networks
# Homework 6
#######################################

from socket import *
import sys
import time
import datetime

#######################################
# Workflow:
# 1. Open UDP Socket
# 2. 10 times:
#          Start timer, send message
#          Receiver Echo & end timer
class UDPClient:

    def __init__(self, udp_host, udp_port):
        self.udp_host = udp_host
        self.udp_port = udp_port
        self.start()

    def start(self):
        # 1. First, connect to python UDP
        clientSock = socket(AF_INET, SOCK_DGRAM)
        # 2. Set a timeout on blocking socket operations
        clientSock.settimeout(5)
        # 3. Create an address tuple from host-port
        addr = (self.udp_host, self.udp_port)
        # 4. Create a message
        msg = "Hi!"
        # 5. Encode it for sending during the ping
        encoded_msg = msg.encode('utf-8')
        
        # Ping the address 10 times
        for i in range(0,10):
            # Use the .sendto function to send the encoded message to the address we created
            clientSock.sendto(encodeMsg, addr)       
            # Create and set a start time for the tmer
            start = time.time()

            try:
                # Get the message and server address
                msg, addr = clientSock.recvfrom(1024)
                # Calculate round trip time (RTT) by finding current time and subtracting
                end = time.time()
                rtt = end - start
                cur_time = time.localtime()
                print("Reply from " + addr[0] + ": PING " + str(i) + " " + time.asctime(cur_time))
                print("\nRTT: " + str(rtt))

            except:
                self.timeout()
                continue
    
    # Simple time-out function
    def timeout(self):
        print("Request has timed out.")

def main():

    print (sys.argv, len(sys.argv))

    udp_host = 'localhost'
    udp_port = 50007

    if len(sys.argv) > 1:
        udp_host = sys.argv[1]
        udp_port = int(sys.argv[2])

    udpclient = UDPClient(udp_host, udp_port)

if __name__ == '__main__':
    main() 
