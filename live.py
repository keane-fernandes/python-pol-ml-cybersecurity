""""

This is a python utility to capture packets live over the Automotive Rig v1.0 from Thales.
The user needs to define only ONE of the following:
    1. The number of packets 
                OR
    2. The timeout in seconds

"""

import pyshark as ps
import collections
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pol_utilities as pu

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

# IMPORTANT : change the interface for your system
capture = ps.LiveCapture(interface="en5", only_summaries=False)

# Iterate though packets and populate the list of packet parameters
for packet in capture.sniff_continuously(packet_count=150000):
    spatiotemporal = []
    packet_date_time = str(packet.frame_info.time)
    date = pu.extract_date(packet_date_time)
    time = pu.extract_time(packet_date_time)
    location = pu.extract_location(packet_date_time)

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
masterPacketList.to_csv("./live.csv", index=False)
