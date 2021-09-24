#!/usr/bin/env python3

from _thread import *
import threading

import socket
import signal
import sys

PORT = int(sys.argv[1])
PATH = sys.argv[2]
HOST = '0.0.0.0'

def handler(signum, frame):
    sys.stderr.write('Signal handler called with signal', signum)
    exit(0)

signal.signal(signal.SIGQUIT, handler)
signal.signal(signal.SIGTERM, handler)
signal.signal(signal.SIGINT, handler)

thread_lock = threading.Lock()

def thread_client(client, connection_id):
    complete_message = b''
    
    while True:
        try:
            data = client.recv(4096)
        except:
            
            file_name = "." + PATH + "/" + str(connection_id) + ".file"
            file = open(file_name, 'wb')
            file.write(b"ERROR: The connection timed out.")
            file.close()
            
            client.close()
            thread_lock.release()
            break
        
        if not data:
            file_name = "." + PATH + "/" + str(connection_id) + ".file"
            file = open(file_name, 'wb')
            index = complete_message.find(b'\r\n\r\n')
            file.write(complete_message[index+4:])
            file.close()
            
            thread_lock.release()
            break
            
        complete_message += data
        

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #crates socket
soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #in case socket is already open
soc.settimeout(10)

try:
    soc.bind((HOST, PORT)) #binds socket
except:
    sys.stderr.write("ERROR: Port number not available.\n")
    exit(1)
    
soc.listen(10)
#soc.setblocking(False)

connection_id = 0

while True:
    
    client, address = soc.accept()
    client.settimeout(10)
    
    connection_id += 1
    
    thread_lock.acquire()
    
    start_new_thread(thread_client, (client, connection_id))

soc.close()
