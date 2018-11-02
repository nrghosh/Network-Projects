#
# COMP 332, Spring 2018
# Chat client

# Nikhil Ghosh

import socket
import sys
import threading


class ChatClient:

    def __init__(self, chat_host, chat_port):
        self.chat_host = chat_host
        self.chat_port = chat_port
        self.name = input("Enter username: ")
        self.start()

    def start(self):

        # Open connection to chat
        try:
            chat_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            chat_sock.connect((self.chat_host, self.chat_port))
            print("Connected to socket")
        except OSError as e:
            print("Unable to connect to socket: ")
            if chat_sock:
                chat_sock.close()
            sys.exit(1)

        threading.Thread(target=self.write_sock, args=(chat_sock,)).start()
        threading.Thread(target=self.read_sock, args=(chat_sock,)).start()

    def reformat(self, data):
        size = str(len(data))
        name = self.name
        # Use string flags for later on (to isolate size, username, etc)
        return ("message_size: " + size + "sizeflag username: " + name + "endflag end_header" + data).encode("utf-8") 

    def find_thing(self, msg, thing, end):
        # Utility function: find an element of a message
        try:
            front_thing = msg.find(thing)
            end_thing = front_thing + len(thing)
            field_end = end_thing + msg[end_thing: ].index(end)
            val = msg[end_thing : field_end]
            return val
        except ValueError:
            print("Item not found!")
            return -1

    def write_sock(self, sock):
        while True:
            msg = input()
            segment = self.reformat(msg)
            sock.sendall(segment)

        print("In write sock")

    def read_sock(self, sock):
        data = b''
        while True:
            data += (sock.recv(4096))
            msg = data.decode("utf-8")
            try:
                user = self.find_thing(msg, "username: ", "endflag")
                size = int(self.find_thing(msg, "message_size: ", "sizeflag"))
                msg_start = msg.find("end_header") + len("end_header")
                msg_end = msg_start + size
                
                if len(msg) >= int(msg_end):
                    print(user + ": " + msg[msg_start: msg_end])
                data = data[msg_end :]
            except ValueError:
                print("Value Error")                  
        print("In read sock")

def main():

    print (sys.argv, len(sys.argv))
    chat_host = "localhost"
    chat_port = 50007

    if len(sys.argv) > 1:
        chat_host = sys.argv[1]
        chat_port = int(sys.argv[2])

    chat_client = ChatClient(chat_host, chat_port)

if __name__ == '__main__':
    main()
