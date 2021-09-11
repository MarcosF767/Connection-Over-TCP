#!/usr/bin/env python3

import os
import sys
import socket

HOST = sys.argv[1]
PORT = sys.argv[2]
FILE = sys.argv[3]

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.settimeout(10)

in_message = ""

try:
    soc.connect((HOST, int(PORT)))
except:
    sys.stderr.write("ERROR: Not able to connect to the provided host and port.\n")
    soc.close()
    exit(1)

while(not("accio\r\n" in in_message)):
    recieved = soc.recv(1024)
    in_message = in_message + recieved.decode('utf-8')

read_pointer = 0
f = open(FILE, 'rb')
f.seek(0, os.SEEK_END)
size_of_file = f.tell()
print(size_of_file)

while(read_pointer < size_of_file):
    f.seek(read_pointer)
    try:
        sent = soc.send(f.read(10000))
        print("sent " + str(sent) + " bytes")
    except:
        sys.stderr.write("ERROR: Connection disconnected while sending the file.\n")
        soc.close()
        exit(1) #sys.exit(1)
    read_pointer += 10000
    
soc.close()
