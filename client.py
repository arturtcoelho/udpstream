import socket
import datetime

clientAddress = ("127.0.0.1", 7070)

# Create a datagram based server socket that uses IPv4 addressing scheme
datagramSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
datagramSocket.bind(clientAddress)

while(True):
    n, sourceAddress = datagramSocket.recvfrom(128)
    print(n.decode())