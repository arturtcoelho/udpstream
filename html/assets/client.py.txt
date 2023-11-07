import socket
import argparse
import logging
import numpy as np

# Parse command-line arguments using argparse
parser = argparse.ArgumentParser(description="UDP Client")
parser.add_argument('--log_file', type=str, default=None, help="Log file path (optional)")
parser.add_argument('--verbose', action='store_true', help="Enable verbose logging (optional)")
parser.add_argument('--server_port', type=int, default=7070, help="Server port (optional)")
parser.add_argument('client_id', type=int, help="Client ID")
args = parser.parse_args()

# Extract command-line arguments
log_file = args.log_file
verbose = args.verbose
serverPort = args.server_port
clientId = args.client_id

# Set up the logging configuration
logging.basicConfig(level=logging.DEBUG if verbose else logging.INFO,
                    format=f' client {clientId} | %(asctime)s %(levelname)-8s %(message)s',
                    filename=log_file)

# Create a logger instance
logger = logging.getLogger('udp_client')

# Log client startup
logger.info(f"Starting UDP client {clientId}")

# Define server address and set up the socket
serverAddress = (serverIp, serverPort) = ("127.0.0.1", serverPort)
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
clientSocket.settimeout(5)  # 5 seconds timeout

# Register with the server
clientSocket.sendto(b"register", serverAddress)
logger.info(f"Sent register message to server {serverIp}:{serverPort}")

packetData = []
sensorData = []

try:
    while True:
        packet, serverAddress = clientSocket.recvfrom(1024)
        if packet.decode() == 'end':
            logger.info('Got end of transmission')
            break
        number, data = map(int, packet.decode().split())

        # Log received packet and data
        logger.debug(f"Received packet {number}: {data}")

        packetData.append(number)
        sensorData.append(data)

except socket.timeout:
    logger.warning("Server has not responded in 5 seconds, closing the client socket")
except KeyboardInterrupt:
    clientSocket.sendto(b"quit", serverAddress)
    logger.info(f"Sent quit message to server {serverIp}:{serverPort}")

clientSocket.close()

# Sort packet data and find the first packet number
orderedPacketData = sorted(packetData)
firstPacket = orderedPacketData[0]

# Count out-of-order packets
def count_out_of_order(arr):
    out_of_order_count = 0

    for i in range(len(arr) - 1):
        if arr[i] > arr[i + 1]:
            out_of_order_count += 1

    return out_of_order_count

# Log lost and out-of-order packets
lost_packets = len(set(range(firstPacket, firstPacket + len(packetData))) - set(packetData)) + firstPacket - 1
out_of_order_packets = count_out_of_order(packetData)
logger.info(f"Lost packets: {lost_packets}")
logger.info(f"Out of order packets: {out_of_order_packets}")

# Calculate standard deviation of sensor data
standard_deviation = np.std(sensorData)
logger.info(f"Standard deviation: {standard_deviation}")
