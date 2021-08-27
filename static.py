""""
Name: static.py

Hardware: Automotive Rig v1.0 from Thales

Description: This is a python utility that automatically parses specified capture files and 
outputs the data to a .csv file and stores it in the pol_profiles directory. If the 
directory does not exist, it will be created in the current working directory.

User Input: The user will need to provide the name of the profile being created 
using a string as an argument when opening the file.

"""
import pyshark as ps
import numpy as np
import pandas as pd
import pol_utilities as pu
import os
import directories as dirs


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

# Define input and output folder paths
cwd = os.getcwd()
input_folder_path = os.path.join(cwd, dirs.root.get("testing"))
output_folder_path = os.path.join(cwd, dirs.root.get("preprocessed"))

# Files in their raw form (.pcapng)
files_to_process = [
    f
    for f in os.listdir(input_folder_path)
    if os.path.isfile(os.path.join(input_folder_path, f))
    if f.endswith(".pcapng")
]

# Files that have been already preprocessed (.csv)
completed = [
    d
    for d in os.listdir(output_folder_path)
    if os.path.isfile(os.path.join(output_folder_path, d))
    if d.endswith(".csv")
]

# files_to_process list and completed list are compared, and if a file does not
# exist in completed, it undergoes parsing and preprocessing
for the_file in files_to_process:
    if not pu.check_if_preprocessed(the_file, completed):
        # Create the dataframes for the different kinds of packets
        master_packets = pd.DataFrame(columns=packet_attributes)

        # Import the .pcapng file
        filePath = os.path.join(input_folder_path, the_file)
        capture = ps.FileCapture(filePath, only_summaries=False, keep_packets=False)

        print("Currently processing: {}".format(the_file))
        # Iterate though packets and populate the above declared dataframes
        for packet in capture:
            packet_date_time = pd.to_datetime(str(packet.frame_info.time))
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
                master_packets = master_packets.append(df_temp, ignore_index=True)

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
                master_packets = master_packets.append(df_temp, ignore_index=True)

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
                master_packets = master_packets.append(df_temp, ignore_index=True)

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
                master_packets = master_packets.append(df_temp, ignore_index=True)

            else:
                print("Uknown packet encountered!")
                pass

        print("Packets processed: " + str(len(master_packets.index)))

        # Write the newly parsed file to the 01_pol_preprocessed directory
        new_csv_filename = str(os.path.splitext(the_file)[0]) + ".csv"
        new_csv_path = os.path.join(output_folder_path, new_csv_filename)

        master_packets.index.name = "PacketNumber"
        master_packets.to_csv(new_csv_path, index=False)
