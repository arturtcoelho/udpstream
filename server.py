# ----- An UDP streaming server in Python that sends sensor reading values -----

import json
import socket
import sys
import time
import threading

from log import log

try:
    timer = float(sys.argv[1])
except Exception:
    timer = 0.1

try:
    log_file = sys.argv[2]
except Exception:
    log_file = 'server.log'

serverAddress = (serverIp, serverPort) = ("127.0.0.1", 7070)

# Create a datagram based server socket that uses IPv4 addressing scheme
datagramSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
datagramSocket.bind(serverAddress)

# Load the sensor data from the file
with open("data.json", "r") as f:
    sensorData = json.load(f)

packetNumber = 0

print(f"UDP server is streaming on {serverIp}:{serverPort}")

# A set of clients that are registered to receive the sensor data
clients = set()


def wait_for_new_clients():
    try:
        while True:
            data, address = datagramSocket.recvfrom(1024)
            if data == b"register":
                clients.add(address)
                log(f"Registered client {address}", log_file)
            if data == b"quit":
                clients.remove(address)
                log(f"Removed client {address}", log_file)

    # If the socket is closed, stop the thread
    except OSError:
        log("Server is shutting down", log_file)

# Send the message to all registered clients
def send_to_clients(message):
    if len(clients) > 0:
        for client in clients:
            datagramSocket.sendto(message, client)
            # log(f"Sent {message} to {client}", log_file)

# Register a thread that waits for new clients
butler = threading.Thread(target=wait_for_new_clients)
butler.start()

# Wait for new clients to register
log("Waiting for any client to register...", log_file)
while len(clients) == 0:
    time.sleep(1)

try:
    # Start streaming the sensor data
    for item in sensorData:
        # Send the data to the client
        packetNumber += 1
        message = f"{packetNumber} {item}".encode()
        send_to_clients(message)

        time.sleep(timer)
    send_to_clients('end'.encode())
except KeyboardInterrupt:
    send_to_clients('end'.encode())

datagramSocket.close()

try:
    butler.join()
except KeyboardInterrupt:
    log("Server is shutting down", log_file)
