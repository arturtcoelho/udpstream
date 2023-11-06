import json
import socket
import sys
import time
import threading
import argparse
import logging

# Parse command-line arguments using argparse
parser = argparse.ArgumentParser(description="UDP Streaming Server")
parser.add_argument('--timer', type=float, default=0.1, help="Time delay between data packets (optional)")
parser.add_argument('--log_file', type=str, default=None, help="Log file path (optional)")
parser.add_argument('--verbose', action='store_true', help="Enable verbose logging (optional)")
parser.add_argument('--port', type=int, default=7070, help="Server port (optional)")
args = parser.parse_args()

# Extract command-line arguments
timer = args.timer
log_file = args.log_file
verbose = args.verbose
serverPort = args.port

# Set up the logging configuration
logging.basicConfig(level=logging.DEBUG if verbose else logging.INFO,
                    format=' server   | %(asctime)s %(levelname)-8s %(message)s',
                    filename=log_file)

# Create a logger instance
logger = logging.getLogger('udp_streaming_server')

# Define the server address
serverAddress = (serverIp, serverPort) = ("127.0.0.1", serverPort)

# Log server startup
logger.info(f"Starting UDP server on {serverIp}:{serverPort}")

# Create a datagram-based server socket using IPv4 addressing scheme
datagramSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
datagramSocket.bind(serverAddress)

# Load sensor data from a JSON file
with open("data.json", "r") as f:
    sensorData = json.load(f)

# Initialize packet number and a set of registered clients
packetNumber = 0
clients = set()

# Function to wait for new clients to register
def wait_for_new_clients():
    try:
        while True:
            data, address = datagramSocket.recvfrom(1024)
            ip, port = address

            if data == b"register":
                clients.add(address)
                logger.info(f"Registered client {ip}:{port}")

            if data == b"quit":
                clients.remove(address)
                logger.info(f"Removed client {ip}:{port}")

    except OSError:
        logger.info("Server is shutting down")

# Function to send a message to all registered clients
def send_to_clients(message):
    if len(clients) > 0:
        for client in clients:
            ip, port = client
            datagramSocket.sendto(message, client)
            logger.debug(f"Sent message '{message.decode()}' to {ip}:{port}")

# Start a thread to wait for new clients
butler = threading.Thread(target=wait_for_new_clients)
butler.start()

# Wait for at least one client to register
logger.info("Waiting for any client to register...")
while len(clients) == 0:
    time.sleep(1)

logger.info("Streaming started")

try:
    # Start streaming the sensor data
    for item in sensorData:
        # Send the data to the clients
        packetNumber += 1
        message = f"{packetNumber} {item}".encode()
        send_to_clients(message)
        time.sleep(timer)
    send_to_clients(b'end')

except KeyboardInterrupt:
    send_to_clients(b'end')

logger.info("Streaming finished")
datagramSocket.close()

try:
    butler.join()
except KeyboardInterrupt:
    logger.info("Server is shutting down")
