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
    print("here 1 ")
    sock = key.fileobj
    connection, address = sock.accept()
    connection.setblocking(False)
    connection.settimeout(10)
    #rsp = sock.send(b"accio\r\n")
    data = Client(address)
    data.outb = b'accio\r\n'
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    selector.register(connection, events, data=data)
    
def service(key, event):
    sock = key.fileobj
    data = key.data
    #print("here 2 ")
    if event & selectors.EVENT_READ:
        #print('-----------HERE service Read-------------')
        recieved_data = sock.recv(4096)
        if recieved_data:
            data.inb += recieved_data
            print(data.inb.decode('utf-8'))
        else:
            print('closing connection to', data.addr)
            selector.unregister(sock)
            sock.close()
    if event & selectors.EVENT_WRITE:
        #print('-----------HERE service Write-------------')
        if data.outb:
            sent = sock.send(data.outb)
            data.outb = data.outb[sent:]

PORT = int(sys.argv[1])
HOST = '0.0.0.0'

not_stopped = True

signal.signal(signal.SIGQUIT, handler)
signal.signal(signal.SIGTERM, handler)
signal.signal(signal.SIGINT, handler)


soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #crates socket
soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #in case socket is already open
soc.settimeout(10)

try:
    soc.bind((HOST, PORT)) #binds socket
except:
    sys.stderr.write("ERROR: Port number not available.\n")
    exit(1)

soc.listen(20)
soc.setblocking(False)

selector = selectors.DefaultSelector()
selector.register(soc, selectors.EVENT_READ, data=None)

while not_stopped:
    #print("--------------HERE loop-------------------")
    events = selector.select(timeout = 10)
    for key, event in events:
        if key.data is None:
            #print("--------------HERE 5-------------------")
            accept(key)
        else:
            #print("--------------HERE 6-------------------")
            service(key, event)
            
soc.close()

