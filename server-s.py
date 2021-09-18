#!/usr/bin/env python3

#Server
import selectors
import socket
import signal
import time
import sys


def handler(signum, frame):
    sys.stderr.write('Signal handler called with signal', signum)
    exit(1)

class Client:
    def __init__(self, addr):
        self.addr = addr
        self.inb = b""
        self.outb = b""
        self.last_active = time.time()
    def setTime(self, new_time):
        self.last_active = new_time
        
def accept(key):
    sock = key.fileobj
    connection, address = sock.accept()
    connection.setblocking(False)
    data = Client(address)
    data.outb = b'accio\r\n'
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    selector.register(connection, events, data=data)
    
def service(key, event):
    sock = key.fileobj
    data = key.data
    
    if(time.time() - data.last_active > 10):
        sys.stderr.write("ERROR: The connection has timed out.")
        selector.unregister(sock)
        sock.close()

    if event & selectors.EVENT_READ:
        try:
            recieved_data = sock.recv(4096)
        except TimeoutError:
            sys.stderr.write("ERROR: The connection has timed out.")
            
        if recieved_data:
            data.setTime(time.time())
            data.inb += recieved_data
        else:
            index = data.inb.find(b'\r\n\r\n')
            print(len(data.inb[index+4:]))
            selector.unregister(sock)
            sock.close()
    if event & selectors.EVENT_WRITE:
        if data.outb:
            data.setTime(time.time())
            sent = sock.send(data.outb)
            data.outb = b''

PORT = int(sys.argv[1])
HOST = '0.0.0.0'

not_stopped = True

signal.signal(signal.SIGQUIT, handler)
signal.signal(signal.SIGTERM, handler)
signal.signal(signal.SIGINT, handler)


soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #crates socket
soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #in case socket is already open
#soc.settimeout(10)

try:
    soc.bind((HOST, PORT)) #binds socket
except:
    sys.stderr.write("ERROR: Port number not available.\n")
    exit(1)

soc.listen(10)
soc.setblocking(False)

selector = selectors.DefaultSelector()
selector.register(soc, selectors.EVENT_READ, data=None)

while not_stopped:
    events = selector.select(timeout=10)
    for key, event in events:
        if key.data is None:
            accept(key)
        else:
            service(key, event)
            
soc.close()
