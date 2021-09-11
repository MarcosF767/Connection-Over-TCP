#!/usr/bin/env python3

import sys

HOST = sys.argv[1]
PORT = sys.argv[2]
FILE = sys.argv[3]

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

soc.connect((HOST, PORT))

soc.close()
