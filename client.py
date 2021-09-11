#!/usr/bin/env python3

import sys
import socket

HOST = sys.argv[1]
PORT = sys.argv[2]
FILE = sys.argv[3]

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    soc.connect((HOST, int(PORT)))
except:
    sys.stderr.write("ERROR: Not able to connect to the provided host and port.\n")
    sys.exit(1)

sys.stderr.write("success")

soc.close()
