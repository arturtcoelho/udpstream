# ----- An UDP client in Python that sends temperature values to server-----

import socket
import time
import sys


try:
    timer = float(sys.argv[1])
except Exception:
    timer = 1

# A tuple with server ip and port
serverAddress = ("127.0.0.1", 7070)

# Create a datagram socket

mySocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

packNum = 0
while True:

    # Socket is not in connected state yet...sendto() can be used
    # Send temperature to the server

    mySocket.sendto(str(packNum).encode(), ("127.0.0.1",7070))
    packNum+=1

    time.sleep(timer)