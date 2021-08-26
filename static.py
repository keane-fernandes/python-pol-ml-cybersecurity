""""
Name: static.py

Hardware: Automotive Rig v1.0 from Thales

Description: This is a python utility that can parse a specified capture file and 
outputs the data to a .csv file and stores it in the pol_profiles directory. If the 
directory does not exist, it will be created in the current working directory.

User Input: The user will need to provide the name of the profile being created 
using a string as an argument when opening the file.

"""
import pyshark as ps
import collections
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pol_utilities as pu

# Packet lists based on PolPacket class in pol_utilities
vehicleSpeedPackets = []
throttlePedalPackets = []
brakeStatusPackets = []
cruiseControlPackets = []
broadcastPackets = []
maliciousPackets = []
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
masterPacketList = pd.DataFrame(columns=packet_attributes)

# Behaviour Parameters
validPackets = 0
broadcastPackets = 0
maliciousPackets = 0
throughput = 0.0  # packets/sec
time = 0.0

# Import packets from capture file
capture = ps.FileCapture(
    "./pol_raw/CC-true/baseline-1.pcapng", only_summaries=False, keep_packets=False
)

# Iterate though packets and populate PolPacket object
for packet in capture:
    spatiotemporal = []
    packet_date_time = str(packet.frame_info.time)
    packet_length = int(packet.frame_info.len)
    timestamp = float(packet.frame_info.time_relative)
    time_delta = float(packet.frame_info.time_delta)

    if pu.check_for_valid(packet):
        byte_field = packet.udp.payload.split(":")

        sid = pu.extract_sid(byte_field)
        iid = pu.extract_iid(byte_field)

        status_type = pu.compute_status_type(sid, iid)

        payload = pu.extract_payload(byte_field, status_type)

        # UDP Layer data extraction
        source_port = int(packet.udp.srcport)
        destination_port = int(packet.udp.dstport)

        # IP layer data extraction
        source_ip = str(packet.ip.src)
        destination_ip = str(packet.ip.dst)

        entry = [
            packet_date_time,
            status_type,
            timestamp,
            time_delta,
            packet_length,
            source_ip,
            destination_ip,
            source_port,
            destination_port,
            payload,
        ]

        df_temp = pd.DataFrame([entry], columns=packet_attributes)
        masterPacketList = masterPacketList.append(df_temp, ignore_index=True)

    elif pu.check_for_broadcast(packet):
        sid = pu.retrieve_sid("broadcast")
        iid = pu.retrieve_iid("broadcast")

        status_type = pu.compute_status_type(sid, iid)
        entry = [
            packet_date_time,
            status_type,
            timestamp,
            time_delta,
            packet_length,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
        ]

        df_temp = pd.DataFrame([entry], columns=packet_attributes)
        masterPacketList = masterPacketList.append(df_temp, ignore_index=True)

    elif pu.check_for_dhcp(packet):
        sid = pu.retrieve_sid("dhcp")
        iid = pu.retrieve_iid("dhcp")

        status_type = pu.compute_status_type(sid, iid)

        source_port = int(packet.udp.srcport)
        destination_port = int(packet.udp.dstport)

        source_ip = str(packet.ip.src)
        destination_ip = str(packet.ip.dst)

        entry = [
            packet_date_time,
            status_type,
            timestamp,
            time_delta,
            packet_length,
            source_ip,
            destination_ip,
            source_port,
            destination_port,
            np.nan,
        ]

        df_temp = pd.DataFrame([entry], columns=packet_attributes)
        masterPacketList = masterPacketList.append(df_temp, ignore_index=True)

    elif pu.check_for_ssdp(packet):
        sid = pu.retrieve_sid("ssdp")
        iid = pu.retrieve_iid("ssdp")

        status_type = pu.compute_status_type(sid, iid)

        source_port = int(packet.udp.srcport)
        destination_port = int(packet.udp.dstport)

        source_ip = str(packet.ip.src)
        destination_ip = str(packet.ip.dst)
        entry = [
            packet_date_time,
            status_type,
            timestamp,
            time_delta,
            packet_length,
            source_ip,
            destination_ip,
            source_port,
            destination_port,
            np.nan,
        ]

        df_temp = pd.DataFrame([entry], columns=packet_attributes)
        masterPacketList = masterPacketList.append(df_temp, ignore_index=True)
    else:
        pass


print("Training Statistics:")
print("Packets processed: " + str(len(masterPacketList.index)))

masterPacketList.index.name = "PacketNumber"
masterPacketList.to_csv("./output.csv", index=False)
