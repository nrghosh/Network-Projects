#
# COMP 332, Spring 2018
# Chat server

# Nikhil Ghosh

import socket
import sys
import threading

class ChatProxy():

    def __init__(self, server_host, server_port):
        self.server_host = server_host
        self.server_port = server_port
        self.server_backlog = 1
        self.chat_list = {}
        self.chat_id = 0
        self.lock = threading.Lock()
        self.start()

    def start(self):

        # Initialize server socket on which to listen for connections
        try:
            server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_sock.bind((self.server_host, self.server_port))
            server_sock.listen(self.server_backlog)
        except OSError as e:
            print ("Unable to open server socket")
            if server_sock:
                server_sock.close()
            sys.exit(1)

        # Wait for user connection
        while True:
            conn, addr = server_sock.accept()
            self.add_user(conn, addr)
            thread = threading.Thread(target = self.serve_user,
                    args = (conn, addr, self.chat_id))
            thread.start()

    def add_user(self, conn, addr):
        print ('User has connected', addr)
        self.chat_id = self.chat_id + 1
        self.lock.acquire()
        self.chat_list[self.chat_id] = (conn, addr)
        self.lock.release()

    def find_thing(self, msg, thing, end):
        try:
            front_thing = msg.find(thing)
            end_thing = front_thing + len(thing)
            field_end = end_thing + msg[end_thing: ].index(end)
            val = msg[end_thing : field_end]
            return val
        except ValueError:
            print("Item not found!")
            return -1

    def read_data(self, conn):
        raw_data = b''
        while True:
            raw_data += (conn.recv(4096))
            msg = raw_data.decode('utf-8')
            try:
                size = int(self.find_thing(msg, 'message_size: ', 'sizeflag'))
                msg_start = msg.find('end_header') + len('end_header')
                msg_end = msg_start + size
                data = data[msg_end :]
                
                return (msg[: msg_end]).encode('utf-8')
            except ValueError:
                print("Value Error")
                     
        print("In read data")

        return data

    def send_data(self, user, data):
        self.lock.acquire()
        for i in self.chat_list:
            if i != user:
                (self.chat_list[i][0]).sendall(data)
        self.lock.release()

    def cleanup(self, conn, user):
        self.lock.acquire()
        (self.chat_list).pop(user)
        print("In cleanup")

        self.lock.release()

    def serve_user(self, conn, addr, user):
        while True:
            data = self.read_data(conn)
            print("serve_user function has received: " + (data).decode('utf-8'))
            if (data).decode('utf-8') == "":
                self.cleanup(conn, user)
                print(str(user) + " removed from chat list")
                return               
            self.send_data(user, data)
            print("In serve user")


def main():

    print (sys.argv, len(sys.argv))
    server_host = 'localhost'
    server_port = 50007

    if len(sys.argv) > 1:
        server_host = sys.argv[1]
        server_port = int(sys.argv[2])

    chat_server = ChatProxy(server_host, server_port)

if __name__ == '__main__':
    main()
