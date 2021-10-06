""""

Hardware:       Automotive Rig v1.0 from Thales
Description:    This is a python utility that contains helper methods and constants
                to aid 01_collect.py and 02_feature.py.


User Iput:      None required.
Usage:          It is a helper file, cannot be opened directly.

"""

# Packet lists based on PolPacket class in pol_utilities
packet_attributes = [
    "DateTime",
    "StatusType",
    "Timestamp",
    "TimeDelta",
    "PacketLength",
    "SourceIP",
    "DestinationIP",
    "SourcePort",
    "DestinationPort",
    "Payload",
]

# Project folders
root = {
    "raw": "00_raw",
    "collect": "01_collect",
    "feature": "02_features",
    "train": "03_train",
    "plot": "05_plots",
    "testing": "06_testing",
    "live_raw": "07_live_raw",
    "live_collect": "08_live_collect",
    "live_feature": "09_live_features",
    "live_throughput": "10_live_throughputs",
    "live_plot": "11_live_plot",
    "raw_test": "10_raw",
    "collect_test": "11_collect",
    "feature_test": "12_feature",
    "plot_test": "15_plot",
    "input": "98_input",
    "output": "99_output",
}

# Libraries
import os

# General constants
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


# Vehicle Speed Status Packet (Packet and UDP lengths are different from default)
__VEHICLESPEEDSTATUS_STATUS_ID = "SPEED"
__VEHICLESPEEDSTATUS_LENGTH = 130
__VEHICLESPEEDSTATUS_UDP_LENGTH = 96
__VEHICLESPEEDSTATUS_SID = "aa00aba4"  # Hexadecimal
__VEHICLESPEEDSTATUS_IID = "55005731"  # Hexadecimal
__VEHICLESPEEDSTATUS_PAYLOAD_LENGTH = 16
__VEHICLESPEEDSTATUS_SPEED_END_BYTE = 8

# Throttle Status Packet
__THROTTLESTATUS_STATUS_ID = "THROTTLE"
__THROTTLEPEDALSTATUS_SID = "aa00aba1"  # Hexadecimal
__THROTTLEPEDALSTATUS_IID = "5500572e"  # Hexadecimal
__THROTTLEPEDALSTATUS_DEMAND_END_BYTE = 8

# Brake Status Packet
__BRAKESTATUS_STATUS_ID = "BRAKE"
__BRAKESTATUS_SID = "aa00abc2"  # Hexadecimal
__BRAKESTATUS_IID = "5500574f"  # Hexadecimal
__BRAKESTATUS_END_BYTE = 2

# Cruise Control Status Packet
__CRUISECONTROL_STATUS_ID = "CRUISE"
__CRUISECONTROLSTATUS_SID = "aa00ab9b"  # Hexadecimal
__CRUISECONTROLSTATUS_IID = "55005728"  # Hexadecimal
__CRUISECONTROL_END_BYTE = 8

# MDNS Packet
__MDNS_STATUS_ID = "MDNS"
__MDNS_SID = "cccccccc"
__MDNS_IID = "cccccccc"

# SSDP Packet
__SSDP_STATUS_ID = "SSDP"
__SSDP_SID = "dddddddd"
__SSDP_IID = "dddddddd"

# DHCP Packet
__DHCP_STATUS_ID = "DHCP"
__DHCP_SID = "eeeeeeee"
__DHCP_IID = "eeeeeeee"

# Broadcast Packet
__RRCP_STATUS_ID = "RRCP"
__RRCP_LENGTH = 60
__RRCP_SID = "ffffffff"
__RRCP_IID = "ffffffff"

# ARP Packet
__ARP_STATUS_ID = "ARP"
__ARP_SID = "gggggggg"
__ARP_IID = "gggggggg"

# NBNS Packet
__NBNS_STATUS_ID = "NBNS"
__NBNS_SID = "hhhhhhhh"
__NBNS_IID = "hhhhhhhh"

# LLMNR Packet
__LLMNR_STATUS_ID = "LLMNR"
__LLMNR_SID = "iiiiiiii"
__LLMNR_IID = "iiiiiiii"

# Malformed packet
__MALFORMED_STATUS_ID = "MALFORMED"
__MALFORMED_SID = "jjjjjjjj"
__MALFORMED_IID = "jjjjjjjj"
__MALFORMED_DEFAULT_LAYERS = 5

# Malicious Packet
__MALICIOUSPACKET_STATUS_ID = "MALICIOUS"
__MALICIOUSPACKET_SID = "mmmmmmmm"
__MALICIOUSPACKET_IID = "mmmmmmmm"

# Checks if a packet is valid (i.e. contains information on vehicle speed
# status, cruise control, brake status or throttle status)
def check_for_valid(packet):

    # Check packet layers
    if not check_number_of_layers(packet, __DEFAULT_PACKET_LAYERS):
        return False
    if not check_for_layers(packet, "eth", "ip", "udp", "data"):
        return False

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


# Checks if a packet matches a broadcast message sent by the input controller
def check_for_rrcp(packet):
    if not check_number_of_layers(packet, __DEFAULT_BROADCAST_LAYERS):
        return False

    if not check_for_layers(packet, "eth", "data"):
        return False

    packet_length = int(packet.frame_info.len)

    if packet_length != __RRCP_LENGTH:
        return False

    return True


# Checks if a packet is sent using the DHCP packet in the network
def check_for_dhcp(packet):
    if check_for_layers(packet, "dhcp") or check_for_layers(packet, "dhcpv6"):
        return True

    return False


# Checks if a packet is sent using the SSDP protocol in the network
def check_for_ssdp(packet):
    if check_for_layers(packet, "ssdp"):
        return True

    return False


# Checks if a packet is sent using the MDNS protocol in the network
def check_for_mdns(packet):
    if check_for_layers(packet, "mdns"):
        return True

    return False


def check_for_arp(packet):
    if check_for_layers(packet, "arp"):
        return True

    return False


def check_for_nbns(packet):
    if check_for_layers(packet, "nbns"):
        return True

    return False


def check_for_llmnr(packet):
    if check_for_layers(packet, "llmnr"):
        return True

    return False


def check_for_malformed(packet):
    if not check_number_of_layers(packet, __MALFORMED_DEFAULT_LAYERS):
        return False

    if not check_for_layers(packet, "eth", "udp", "ip", "classicstun", "_ws.malformed"):
        return False

    return True


# Checks that layers exist in a packet
def check_for_layers(packet, *layers):
    for layer in layers:
        if not hasattr(packet, layer):
            return False
    return True


# Checks that a packet has a specified number of layers returning a boolean
def check_number_of_layers(packet, number):
    packetLayers = packet.layers
    packetLayersCount = len(packetLayers)

    if packetLayersCount != number:
        return False
    return True


# Defines a status type depending on the sid, iid
def compute_status_type(sid, iid):
    if sid == __VEHICLESPEEDSTATUS_SID and iid == __VEHICLESPEEDSTATUS_IID:
        return __VEHICLESPEEDSTATUS_STATUS_ID

    if sid == __THROTTLEPEDALSTATUS_SID and iid == __THROTTLEPEDALSTATUS_IID:
        return __THROTTLESTATUS_STATUS_ID

    if sid == __BRAKESTATUS_SID and iid == __BRAKESTATUS_IID:
        return __BRAKESTATUS_STATUS_ID

    if sid == __CRUISECONTROLSTATUS_SID and iid == __CRUISECONTROLSTATUS_IID:
        return __CRUISECONTROL_STATUS_ID

    if sid == __RRCP_SID and iid == __RRCP_IID:
        return __RRCP_STATUS_ID

    if sid == __DHCP_SID and iid == __DHCP_IID:
        return __DHCP_STATUS_ID

    if sid == __SSDP_SID and iid == __SSDP_IID:
        return __SSDP_STATUS_ID

    if sid == __MDNS_SID and iid == __MDNS_IID:
        return __MDNS_STATUS_ID

    if sid == __ARP_SID and iid == __ARP_IID:
        return __ARP_STATUS_ID

    if sid == __NBNS_SID and iid == __NBNS_IID:
        return __NBNS_STATUS_ID

    if sid == __LLMNR_SID and iid == __LLMNR_IID:
        return __LLMNR_STATUS_ID

    if sid == __MALFORMED_SID and iid == __MALFORMED_IID:
        return __MALFORMED_STATUS_ID

    return __MALICIOUSPACKET_STATUS_ID


# Calculates the throughput of a network in packets/second
def calculate_packet_throughput(packets, time):
    throughput = 0
    try:
        throughput = packets / time
    except ZeroDivisionError:
        return 0


# Returns a concatenated string of bytes between start_byte (inclusive) and end_byte (not inclusive)
def extract_bytes(byte_field, start_byte, end_byte):
    return "".join(byte_field[start_byte:end_byte])


# Returns SID from the Service Message Header
def extract_sid(byte_field):
    return extract_bytes(byte_field, __DEFAULT_SID_START_BYTE, __DEFAULT_SID_END_BYTE)


# Returns IID from the Service Message Header
def extract_iid(byte_field):
    return extract_bytes(byte_field, __DEFAULT_IID_START_BYTE, __DEFAULT_IID_END_BYTE)


# Returns an sid based on a specified packet type
def retrieve_sid(packet_type):

    if packet_type == "rrcp":
        return __RRCP_SID
    elif packet_type == "dhcp":
        return __DHCP_SID
    elif packet_type == "ssdp":
        return __SSDP_SID
    elif packet_type == "mdns":
        return __MDNS_SID
    elif packet_type == "arp":
        return __ARP_SID
    elif packet_type == "nbns":
        return __NBNS_SID
    elif packet_type == "llmnr":
        return __LLMNR_SID
    elif packet_type == "malformed":
        return __MALFORMED_SID
    else:
        return __MALICIOUSPACKET_SID


# Returns an iid based on a specified packet type
def retrieve_iid(packet_type):
    if packet_type == "rrcp":
        return __RRCP_IID
    elif packet_type == "dhcp":
        return __DHCP_IID
    elif packet_type == "ssdp":
        return __SSDP_IID
    elif packet_type == "mdns":
        return __MDNS_IID
    elif packet_type == "arp":
        return __ARP_IID
    elif packet_type == "nbns":
        return __NBNS_IID
    elif packet_type == "llmnr":
        return __LLMNR_IID
    elif packet_type == "malformed":
        return __MALFORMED_IID
    else:
        return __MALICIOUSPACKET_IID


# Extracts the payload from the hexdump depending on the status type
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


# ----------------------------------------------------------------
# Feature Extraction
# ----------------------------------------------------------------

chunk_size = 179


def get_behaviour(vehicle_speed, cruise_demand):
    if vehicle_speed == 0:
        return "Stopped"

    if vehicle_speed > 0:
        if cruise_demand > 0:
            return "Cruising"
        return "Moving"

    return "Undefined"


# ----------------------------------------------------------------
# File IO
# ----------------------------------------------------------------


def check_if_preprocessed(filename, processed_list):
    for f in processed_list:
        if os.path.splitext(filename)[0] == os.path.splitext(f)[0]:
            return True
    return False
