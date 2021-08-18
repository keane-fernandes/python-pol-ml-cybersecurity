# Contains helper methods, class definitions and constants to
# aid Pattern of Life (PoL) framework implementation

# There are six types of statuses:
#   0 - Broadcast
#   1 - Vehicle Speed
#   2 - Throttle Pedal
#   3 - Brake Status
#   4 - Cruise Control
#   5 - Unknown / Malicious

# Libraries
import pyshark.packet as p

# Constants

# General
__DEFAULT_PACKET_LENGTH = 122
__DEFAULT_UDP_LENGTH = 88
__DEFAULT_PACKET_LAYERS = 4
__DEFAULT_BROADCAST_LAYERS = 2
__DEFAULT_SID_START_BYTE = 52
__DEFAULT_SID_END_BYTE = 56
__DEFAULT_IID_START_BYTE = 56
__DEFAULT_IID_END_BYTE = 60
__DEFAULT_PAYLOAD_LENGTH = 8
__DEFAULT_FALSE = "00"
__DEFAULT_TRUE = "01"
__DEFAULT_LENGTH = 8

# Broadcast Packet
__BROADCAST_STATUS_ID = 0
__BROADCAST_LENGTH = 60
__BROADCAST_SID = "ffffffff"
__BROADCAST_IID = "ffffffff"

# Vehicle Speed Status Packet (Packet and UDP lengths are different from default)
__VEHICLESPEEDSTATUS_STATUS_ID = 1
__VEHICLESPEEDSTATUS_LENGTH = 130
__VEHICLESPEEDSTATUS_UDP_LENGTH = 96
__VEHICLESPEEDSTATUS_SID = "aa00aba4"  # Hexadecimal
__VEHICLESPEEDSTATUS_IID = "55005731"  # Hexadecimal
__VEHICLESPEEDSTATUS_PAYLOAD_LENGTH = 16
__VEHICLESPEEDSTATUS_SPEED_END_BYTE = 8

# Throttle Status Packet
__THROTTLESTATUS_STATUS_ID = 2
__THROTTLEPEDALSTATUS_SID = "aa00aba1"  # Hexadecimal
__THROTTLEPEDALSTATUS_IID = "5500572e"  # Hexadecimal
__THROTTLEPEDALSTATUS_DEMAND_END_BYTE = 8

# Brake Status Packet
__BRAKESTATUS_STATUS_ID = 3
__BRAKESTATUS_SID = "aa00abc2"  # Hexadecimal
__BRAKESTATUS_IID = "5500574f"  # Hexadecimal
__BRAKESTATUS_END_BYTE = 2

# Cruise Control Status Packet
__CRUISECONTROL_STATUS_ID = 4
__CRUISECONTROLSTATUS_SID = "aa00ab9b"  # Hexadecimal
__CRUISECONTROLSTATUS_IID = "55005728"  # Hexadecimal
__CRUISECONTROL_END_BYTE = 8

# Malicious Packet
__MALICIOUSPACKET_STATUS_ID = 5

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


# Checks that all attributes exist in a layer
def check_attributes_in_layer(layer, *attributes):
    for attribute in attributes:
        if not hasattr(layer, attribute):
            return False

    return True


# Defines a status type (0 - 5) depending on the sid, iid
def compute_status_type(sid, iid):
    if sid == __VEHICLESPEEDSTATUS_SID and iid == __VEHICLESPEEDSTATUS_IID:
        return __VEHICLESPEEDSTATUS_STATUS_ID

    if sid == __THROTTLEPEDALSTATUS_SID and iid == __THROTTLEPEDALSTATUS_IID:
        return __THROTTLESTATUS_STATUS_ID

    if sid == __BRAKESTATUS_SID and iid == __BRAKESTATUS_IID:
        return __BRAKESTATUS_STATUS_ID

    if sid == __CRUISECONTROLSTATUS_SID and iid == __CRUISECONTROLSTATUS_IID:
        return __CRUISECONTROL_STATUS_ID

    if sid == __BROADCAST_SID and iid == __BROADCAST_IID:
        return __BROADCAST_STATUS_ID

    return __MALICIOUSPACKET_STATUS_ID


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

    # Check packet layers
    if not check_number_of_layers(packet, __DEFAULT_PACKET_LAYERS):
        return False
    if not check_for_layers(packet, "eth", "ip", "udp", "data"):
        return False

    # Check layer attributes [IMPORTANT]

    # Check packet and udp payload sizes
    packet_length = int(packet.frame_info.len)
    udp_payload_length = int(packet.udp.length)

    if (
        packet_length != __VEHICLESPEEDSTATUS_LENGTH
        and packet_length != __DEFAULT_PACKET_LENGTH
    ):
        return False

    if (
        udp_payload_length != __DEFAULT_UDP_LENGTH
        and udp_payload_length != __VEHICLESPEEDSTATUS_UDP_LENGTH
    ):
        return False

    return True


# Returns a concatenate string of bytes between start_byte (inclusive) and end_byte (not inclusive)
def extract_bytes(byte_field, start_byte, end_byte):
    return "".join(byte_field[start_byte:end_byte])


# Returns SID from the Service Message Header
def extract_sid(byte_field):
    return extract_bytes(byte_field, __DEFAULT_SID_START_BYTE, __DEFAULT_SID_END_BYTE)


# Returns IID from the Service Message Header
def extract_iid(byte_field):
    return extract_bytes(byte_field, __DEFAULT_IID_START_BYTE, __DEFAULT_IID_END_BYTE)


def get_broadcast_sid():
    return __BROADCAST_SID


def get_broadcast_iid():
    return __BROADCAST_IID


def extract_payload(byte_field, status_type):
    if status_type == __VEHICLESPEEDSTATUS_STATUS_ID:

        payload = extract_bytes(
            byte_field,
            len(byte_field) - __VEHICLESPEEDSTATUS_PAYLOAD_LENGTH,
            len(byte_field),
        )

        speed_hex = payload[0:__VEHICLESPEEDSTATUS_SPEED_END_BYTE]
        speed_decimal = int(speed_hex, 16)
        return speed_decimal

    payload = extract_bytes(
        byte_field,
        len(byte_field) - __DEFAULT_PAYLOAD_LENGTH,
        len(byte_field),
    )

    if status_type == __THROTTLESTATUS_STATUS_ID:
        throttle_demand_hex = payload[0:__THROTTLEPEDALSTATUS_DEMAND_END_BYTE]
        throttle_demand_decimal = int(throttle_demand_hex, 16)
        return throttle_demand_decimal

    if status_type == __BRAKESTATUS_STATUS_ID:
        brake_pressed_hex = payload[0:__BRAKESTATUS_END_BYTE]
        brake_pressed_decimal = int(brake_pressed_hex, 16)
        return brake_pressed_decimal

    if status_type == __CRUISECONTROL_STATUS_ID:
        cruise_control_hex = payload[0:__THROTTLEPEDALSTATUS_DEMAND_END_BYTE]
        cruise_control_decimal = int(cruise_control_hex, 16)
        return cruise_control_decimal


# Checks if a packet matches a broadcast message sent by the input controller
def check_for_broadcast(packet):
    if not check_number_of_layers(packet, __DEFAULT_BROADCAST_LAYERS):
        return False

    if not check_for_layers(packet, "eth", "data"):
        return False

    packet_length = int(packet.frame_info.len)

    if packet_length != __BROADCAST_LENGTH:
        return False

    return True


# ====================================================================
# Helper Methods
# ====================================================================


# Extract relevant information

# A class that holds the attributes required to implement the PoL processing framework
class PolPacket:
    counter = 0

    def __init__(
        self,
        status_type=0,
        timestamp=0,
        time_delta=0,
        packet_length=0,
        source_ip="",
        destination_ip="",
        source_port=0,
        destination_port=0,
        payload=0,
    ):
        self.status_type = status_type
        self.timestamp = timestamp
        self.time_delta = time_delta
        self.packet_length = packet_length  # in bytes
        self.source_ip = source_ip
        self.destination_ip = destination_ip
        self.source_port = source_port
        self.destination_port = destination_port
        self.payload = payload

    # Provides a packet summary
    def print_summary(self):
        print("Packet Summary ")
        print("Status Type: " + str(self.status_type))
        print("Timestamp: " + str(self.timestamp))
        print("Time Delta: " + str(self.time_delta))
        print("Packet Length: " + str(self.packet_length))
        print("Source IP: " + self.source_ip)
        print("Destination IP: " + self.destination_ip)
        print("Source Port: " + str(self.source_port))
        print("Destination Port: " + str(self.destination_port))
        print("Payload: " + str(self.payload))
        print("\n")

    @classmethod
    def increment_packet_counter(cls):
        cls.counter += 1
