# Contains helper methods, class definitions and global constants to
# aid pattern of life implementation

# There are six types of status:
#   0 - Broadcast
#   1 - Vehicle Speed
#   2 - Throttle Pedal
#   3 - Brake Status
#   4 - Cruise Control
#   5 - Unknown

# Libraries
import pyshark.packet as p

# Hexadecimal constants that identify the type of packet
__BRAKESTATUS_SID = "aa00abc2"
__BRAKESTATUS_IID = "5500574f"

__THROTTLEPEDALSTATUS_SID = "aa00aba1"
__THROTTLEPEDALSTATUS_IID = "5500572e"

__VEHICLESPEEDSTATUS_SID = "aa00aba4"
__VEHICLESPEEDSTATUS_IID = "55005731"

__CRUISECONTROLSTATUS_SID = "aa00ab9b"
__CRUISECONTROLSTATUS_IID = "55005728"

# Checks that layers exist in a packet
def check_for_layers(packet, *layers):
    for layer in layers:
        if not hasattr(packet, layer):
            return False
    return True


# Checks that a packet has a specified number of layers
def check_number_of_layers(packet, number):
    packetLayers = packet.layers
    packetLayersCount = len(packetLayers)

    if packetLayersCount != number:
        return False
    return True


def check_attributes_in_layer(layer, *attributes):
    for attribute in attributes:
        if not hasattr(layer, attribute):
            return False

    return True


# Defines a status ID depending on the type of packet sent
def compute_status_type(packet):
    packet_length = packet.frame_info.len

    if packet_length == 60:
        return 0

    if packet_length == 130:
        return 1

    if packet_length == 122:
        return 2


# Calculates the throughput of a network in packets/second
def calculate_packet_throughput(packets, time):
    throughput = 0
    try:
        throughput = packets / time
    except ZeroDivisionError:
        return 0


# Checks if a packet is valid (i.e. contains information on vehicle speed
# status, cruise control, brake status or throttle status)
def check_for_valid(packet):
    if not check_number_of_layers(packet, 4):
        return False
    if not check_for_layers(packet, "eth", "ip", "udp", "data"):
        return False

    packet_length = packet.frame_info.len
    if packet_length != 130 or packet_length != 122:
        return False

    return True


def check_for_vehicle_status(packet):
    pass


def check_for_other(packet):
    pass


# Checks if a packet matches a broadcast message sent by the input controller
def check_for_broadcast(packet):
    if not check_number_of_layers(packet, 2):
        return False

    if not check_for_layers(packet, "eth", "data"):
        return False

    packet_length = packet.frame_info.len

    if packet_length != 60:
        return False

    return True


# Extract relevant information

# A class that holds the attributes required to implement the PoL processing framework
class PolPacket:
    counter = 0

    def __init__(
        self=None,
        hexdump=None,
        status_type=None,
        time_relative=None,
        time_delta=None,
        total_length=None,
        source_ip=None,
        destination_ip=None,
        sid=None,
        iid=None,
        source_port=None,
        destination_port=None,
    ):
        self.hexdump = hexdump
        self.status_type = status_type
        self.time_relative = time_relative
        self.time_delta = time_delta
        self.total_length = total_length  # in bytes
        self.source_ip = source_ip
        self.destination_ip = destination_ip
        self.sid = sid
        self.iid = iid
        self.source_port = source_port
        self.destination_port = destination_port

    # Provides a packet summary
    def print_summary(self):
        print("UDP Statistics")
        print("Hexdump: " + self.hexdump)
        print("Status Type: " + str(self.status_type))
        print("Time Relative: " + self.time_relative)
        print("Time Delta: " + self.time_delta)
        print("Length: " + self.length)
        print("Source Port: " + self.source_port)
        print("Destination Port: " + self.destination_port)
        print("SID: " + self.sid)
        print("IID: " + self.iid)
        print("Source Port: " + self.source_port)
        print("Destination Port: " + self.destination_port)
        print("\n")

    @classmethod
    def increment_packet_counter(cls):
        cls.counter += 1
