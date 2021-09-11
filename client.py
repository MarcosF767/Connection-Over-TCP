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
    exit(1)

try:
    while(not("accio\r\n" in in_message)):
        recieved = soc.recv(1024)
        in_message = in_message + recieved.decode('utf-8')
except:
    sys.stderr.write("ERROR: Connection disconnected while waiting for accio.\n")
    soc.close()
    exit(1)

read_pointer = 0
f = open(FILE, 'rb')
f.seek(0, os.SEEK_END)
size_of_file = f.tell()
print(size_of_file)

header = "Content-Disposition: attachment; filename=\"%s\"\r\nContent-Type: " % FILE + \
    "application/octet-stream\r\nContent-Length: %s\r\n\r\n" % str(size_of_file)
#print(header)

try:
    soc.send(bytes(header, 'UTF-8'))
except:
    sys.stderr.write("ERROR: Connection disconnected while sending the headers.\n")
    f.close()
    soc.close()
    exit(1)

while(read_pointer < size_of_file):
    f.seek(read_pointer)
    try:
        sent = soc.send(f.read(10000))
        #print("sent " + str(sent) + " bytes")
    except:
        sys.stderr.write("ERROR: Connection disconnected while sending the file.\n")
        f.close()
        soc.close()
        exit(1) #sys.exit(1)
    read_pointer += 10000

f.close()
soc.close()