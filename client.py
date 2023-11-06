import socket
import sys

from log import log

try:
    log_file = sys.argv[1]
except Exception:
    log_file = 'client.log'

serverAddress = ("127.0.0.1", 7070)

# Create a datagram based server socket that uses IPv4 addressing scheme
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
clientSocket.settimeout(5)  # 5 seconds timeout

clientSocket.sendto(b"register", serverAddress)

packetData = []
sensorData = []

try:
    while True:
        packet, serverAddress = clientSocket.recvfrom(1024)
        if packet.decode() == 'end':
            log('Got end of transmission', log_file)
            break
        number, data = map(int, packet.decode().split())

        # log(f"Received packet {number}: {data}", log_file)
        packetData.append(number)
        sensorData.append(data)

except socket.timeout:
    log("Server has not responded in 5 seconds, closing the client socket", log_file)
except KeyboardInterrupt:
    clientSocket.sendto(b"quit", serverAddress)

clientSocket.close()

orderedPacketData = sorted(packetData)
firstPacket = orderedPacketData[0]


def count_out_of_order(arr):
    out_of_order_count = 0

    for i in range(len(arr) - 1):
        if arr[i] > arr[i + 1]:
            out_of_order_count += 1

    return out_of_order_count



# Pacotes perdidos:
#   - Pacotes que não foram recebidos devido ao cliente se conectar ao servidor após o envio de alguns pacotes
#   - Pacotes que não foram recebidos devido a perda de pacotes na rede
log(
    f"Pacotes perdidos: {len(set(range(firstPacket, firstPacket + len(packetData))) - set(packetData)) + firstPacket - 1}"
, log_file)

log(f"Pacotes fora de ordem: {count_out_of_order(packetData)}", log_file)

import numpy as np

standard_deviation = np.std(sensorData)
log(f"Desvio padrão: {standard_deviation}", log_file)
