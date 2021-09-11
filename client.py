#!/usr/bin/env python3

import sys
import socket

HOST = sys.argv[1]
PORT = sys.argv[2]
FILE = sys.argv[3]

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

in_message = ""

try:
    soc.connect((HOST, int(PORT)))
except:
    sys.stderr.write("ERROR: Not able to connect to the provided host and port.\n")
    exit(1)

while(not("accio\r\n" in in_message)):
    recieved = soc.recv(1024)
    in_message = in_message + recieved.decode('utf-8')

print(f"recieved {in_message}")
soc.close()
