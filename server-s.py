#!/usr/bin/env python3

#Server
import socket
import selectors
import signal
import sys


def handler(signum, frame):
    sys.stderr.write('Signal handler called with signal', signum)
    exit(1)

class Client:
    def __init__(self, addr):
        self.addr = addr
        self.inb = b""
        self.outb = b""
        
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
    #print("here 2 ")
    if event & selectors.EVENT_READ:
        try:
            recieved_data = sock.recv(4096)
        except TimeoutError:
            print("ERROR: The connection has timed out.")
            
        if recieved_data:
            data.inb += recieved_data
        else:
            print(len(data.inb))
            selector.unregister(sock)
            sock.close()
    if event & selectors.EVENT_WRITE:
        if data.outb:
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
