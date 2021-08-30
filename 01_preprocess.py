""""
Name: preprocess.py

Hardware: Automotive Rig v1.0 from Thales

Description: This is a python utility that automatically parses the capture files and 
outputs the data to a .csv file.

User Input: The user will need to paste the required files into the '00_pol_raw' folder and
the output .csv will be in the '01_pol_preprocessed' folder.

"""
import pyshark as ps
import numpy as np
import pandas as pd
import pol_utilities as pu
import os

# Define input and output folder paths
cwd = os.getcwd()
input_folder_path = os.path.join(cwd, pu.root.get("raw"))
output_folder_path = os.path.join(cwd, pu.root.get("preprocess"))

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
        master_packets = pd.DataFrame(columns=pu.packet_attributes)

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

                df_temp = pd.DataFrame([entry], columns=pu.packet_attributes)
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

                df_temp = pd.DataFrame([entry], columns=pu.packet_attributes)
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

                df_temp = pd.DataFrame([entry], columns=pu.packet_attributes)
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

                df_temp = pd.DataFrame([entry], columns=pu.packet_attributes)
                master_packets = master_packets.append(df_temp, ignore_index=True)

            elif pu.check_for_mdns(packet):
                sid = pu.retrieve_sid("mdns")
                iid = pu.retrieve_iid("mdns")

                status_type = pu.compute_status_type(sid, iid)

                source_port = int(packet.udp.srcport)
                destination_port = int(packet.udp.dstport)

                entry = [
                    packet_date_time,
                    status_type,
                    timestamp,
                    time_delta,
                    packet_length,
                    np.nan,
                    np.nan,
                    source_port,
                    destination_port,
                    np.nan,
                ]
                df_temp = pd.DataFrame([entry], columns=pu.packet_attributes)
                master_packets = master_packets.append(df_temp, ignore_index=True)
            else:
                sid = pu.retrieve_sid("malicious")
                iid = pu.retrieve_iid("malicious")

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
                df_temp = pd.DataFrame([entry], columns=pu.packet_attributes)
                master_packets = master_packets.append(df_temp, ignore_index=True)

        capture.close()
        print("Packets processed: " + str(len(master_packets.index)))

        # Write the newly parsed file to the 01_pol_preprocessed directory
        new_csv_filename = str(os.path.splitext(the_file)[0]) + ".csv"
        new_csv_path = os.path.join(output_folder_path, new_csv_filename)

        master_packets.index.name = "PacketNumber"
        master_packets.to_csv(new_csv_path, index=False)
