#!/usr/bin/env python3

import selectors
import socket

class ClientData:
    def __init__(self, addr):
        self.addr = addr
        self.inb = b'' # input buffer
        self.outb = b'' # output buffer
        
def acceptConnection(sock):
    conn, addr = sock.accept()  # Should be ready to read
    print('accepted connection from', addr)
    conn.setblocking(False)
    data = ClientData(addr)
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)

def serviceConnection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)  # Should be ready to read
        if recv_data:
            data.outb += recv_data
        else:
            print('closing connection to', data.addr)
            sel.unregister(sock)
            sock.close()
            if mask & selectors.EVENT_WRITE:
                if data.outb:
                    print('echoing', repr(data.outb), 'to', data.addr)
                    sent = sock.send(data.outb)  # Should be ready to write
                    data.outb = data.outb[sent:]


HOST = '0.0.0.0'  # The server's hostname or IP address
PORT =  7777        # The port used by the server

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
lsock.bind((HOST, PORT))
lsock.listen(10)
lsock.setblocking(False)

sel = selectors.DefaultSelector()
sel.register(lsock, selectors.EVENT_READ, data=None)

print('listening on', lsock.getsockname())
while True:
    print("--------------HERE 5-------------------")
    events = sel.select(timeout=None)
    for key, mask in events:
        if key.data is None:
            acceptConnection(key.fileobj)
        else:
            serviceConnection(key, mask)

                

