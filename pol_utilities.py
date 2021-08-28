""""

Hardware:       Automotive Rig v1.0 from Thales
Description:    This is a python utility that contains helper methods and constants
                to aid static.py and live.py in implementing the PoL framework.

                There are six types of statuses:
                    AA - Broadcast
                    VS - Vehicle Speed
                    TP - Throttle Pedal
                    BS - Brake Status
                    CC - Cruise Control
                    XX - Unknown / Malicious

User Iput:      None required.
Usage:          It is a helper file, cannot be opened directly.

"""

# Project folders
root = {
    "raw": "00_raw",
    "preprocess": "01_preprocessed",
    "feature": "02_features",
    "testing": "05_testing",
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

# Broadcast Packet
__BROADCAST_STATUS_ID = "B"
__BROADCAST_LENGTH = 60
__BROADCAST_SID = "ffffffff"
__BROADCAST_IID = "ffffffff"

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

# DHCP Packet
__DHCP_STATUS_ID = "DHCP"
__DHCP_SID = "eeeeeeee"
__DHCP_IID = "eeeeeeee"
__DHCP_LENGTH = 342

# SSDP Packet
__SSDP_STATUS_ID = "SSDP"
__SSDP_SID = "dddddddd"
__SSDP_IID = "dddddddd"
__SSDP_LENGTH = 217

# MDNS Packet
__MDNS_STATUS_ID = "MDNS"
__MDNS_SID = "cccccccc"
__MDNS_IID = "cccccccc"
# MDNS has varying lengths hence has been omitted

# Malicious Packet
__MALICIOUSPACKET_STATUS_ID = "M"
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
def check_for_broadcast(packet):
    if not check_number_of_layers(packet, __DEFAULT_BROADCAST_LAYERS):
        return False

    if not check_for_layers(packet, "eth", "data"):
        return False

    packet_length = int(packet.frame_info.len)

    if packet_length != __BROADCAST_LENGTH:
        return False

    return True


# Checks if a packet is sent using the DHCP packet in the network
def check_for_dhcp(packet):
    if check_for_layers(packet, "dhcp"):
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

    if sid == __BROADCAST_SID and iid == __BROADCAST_IID:
        return __BROADCAST_STATUS_ID

    if sid == __DHCP_SID and iid == __DHCP_IID:
        return __DHCP_STATUS_ID

    if sid == __SSDP_SID and iid == __SSDP_IID:
        return __SSDP_STATUS_ID

    if sid == __MDNS_SID and iid == __MDNS_IID:
        return __MDNS_STATUS_ID

    return __MALICIOUSPACKET_STATUS_ID


# Calculates the throughput of a network in packets/second
def calculate_packet_throughput(packets, time):
    throughput = 0
    try:
        throughput = packets / time
    except ZeroDivisionError:
        return 0


# Returns a concatenate string of bytes between start_byte (inclusive) and end_byte (not inclusive)
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

    if packet_type == "broadcast":
        return __BROADCAST_SID
    elif packet_type == "dhcp":
        return __DHCP_SID
    elif packet_type == "ssdp":
        return __SSDP_SID
    elif packet_type == "mdns":
        return __MDNS_SID
    else:
        return __MALICIOUSPACKET_SID


# Returns an iid based on a specified packet type
def retrieve_iid(packet_type):
    if packet_type == "broadcast":
        return __BROADCAST_IID
    elif packet_type == "dhcp":
        return __DHCP_IID
    elif packet_type == "ssdp":
        return __SSDP_IID
    elif packet_type == "mdns":
        return __MDNS_IID
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


# Extract date from a DateTime string from Wireshark
def extract_date(date_time_string):
    string = date_time_string[1 : (len(date_time_string) - 1)]
    string = string.replace(",", "")

    extracted_information = string.split(" ")
    return "-".join(extracted_information[0:3])


# Extract time from a DateTime string from Wireshark
def extract_time(date_time_string):
    string = date_time_string[1 : (len(date_time_string) - 1)]

    extracted_information = string.split(" ")
    return extracted_information[3]


# Extract timezone from a DateTime string from Wireshark
def extract_location(date_time_string):
    string = date_time_string[1 : (len(date_time_string) - 1)]

    extracted_information = string.split(" ")
    return extracted_information[4]


# ----------------------------------------------------------------
# File IO
# ----------------------------------------------------------------


def check_if_preprocessed(filename, processed_list):
    for f in processed_list:
        if os.path.splitext(filename)[0] == os.path.splitext(f)[0]:
            return True
    return False
