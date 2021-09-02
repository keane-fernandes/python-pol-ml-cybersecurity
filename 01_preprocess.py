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
import time


def preprocess():
    # Define input and output folder paths
    cwd = os.getcwd()
    input_folder_path = os.path.join(cwd, pu.root.get("input"))
    output_folder_path = os.path.join(cwd, pu.root.get("output"))

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
            counter = 0
            master_dict = {}

            # Import the .pcapng file
            filePath = os.path.join(input_folder_path, the_file)
            capture = ps.FileCapture(filePath, only_summaries=False, keep_packets=False)

            print("Currently processing: {}".format(the_file))
            # Iterate though packets and populate the above declared dataframes
            for packet in capture:
                packet_dict = {}

                packet_dict["DateTime"] = pd.to_datetime(str(packet.frame_info.time))
                packet_dict["PacketLength"] = int(packet.frame_info.len)
                packet_dict["Timestamp"] = float(packet.frame_info.time_relative)
                packet_dict["TimeDelta"] = float(packet.frame_info.time_delta)

                if pu.check_for_valid(packet):
                    # UDP Layer data extraction and IP layer data extraction
                    packet_dict["SourcePort"] = int(packet.udp.srcport)
                    packet_dict["DestinationPort"] = int(packet.udp.dstport)
                    packet_dict["SourceIP"] = str(packet.ip.src)
                    packet_dict["DestinationIP"] = str(packet.ip.dst)

                    # Dissector methods
                    byte_field = packet.udp.payload.split(":")
                    sid = pu.extract_sid(byte_field)
                    iid = pu.extract_iid(byte_field)

                    status_type = pu.compute_status_type(sid, iid)
                    packet_dict["StatusType"] = status_type
                    packet_dict["Payload"] = pu.extract_payload(byte_field, status_type)

                    master_dict[counter] = packet_dict
                    counter += 1

                elif pu.check_for_broadcast(packet):
                    sid = pu.retrieve_sid("broadcast")
                    iid = pu.retrieve_iid("broadcast")

                    # Irrelevant, but kept in for dataframe uniformity
                    packet_dict["SourcePort"] = np.nan
                    packet_dict["DestinationPort"] = np.nan
                    packet_dict["SourceIP"] = np.nan
                    packet_dict["DestinationIP"] = np.nan

                    packet_dict["StatusType"] = pu.compute_status_type(sid, iid)
                    packet_dict["Payload"] = np.nan

                    master_dict[counter] = packet_dict
                    counter += 1

                elif pu.check_for_dhcp(packet):
                    packet_dict["SourcePort"] = int(packet.udp.srcport)
                    packet_dict["DestinationPort"] = int(packet.udp.dstport)
                    packet_dict["SourceIP"] = str(packet.ip.src)
                    packet_dict["DestinationIP"] = str(packet.ip.dst)

                    sid = pu.retrieve_sid("dhcp")
                    iid = pu.retrieve_iid("dhcp")

                    packet_dict["StatusType"] = pu.compute_status_type(sid, iid)
                    packet_dict["Payload"] = np.nan

                    master_dict[counter] = packet_dict
                    counter += 1

                elif pu.check_for_ssdp(packet):
                    packet_dict["SourcePort"] = int(packet.udp.srcport)
                    packet_dict["DestinationPort"] = int(packet.udp.dstport)
                    packet_dict["SourceIP"] = str(packet.ip.src)
                    packet_dict["DestinationIP"] = str(packet.ip.dst)

                    sid = pu.retrieve_sid("ssdp")
                    iid = pu.retrieve_iid("ssdp")

                    packet_dict["StatusType"] = pu.compute_status_type(sid, iid)
                    packet_dict["Payload"] = np.nan

                    master_dict[counter] = packet_dict
                    counter += 1

                elif pu.check_for_mdns(packet):
                    packet_dict["SourcePort"] = int(packet.udp.srcport)
                    packet_dict["DestinationPort"] = int(packet.udp.dstport)
                    packet_dict["SourceIP"] = np.nan
                    packet_dict["DestinationIP"] = np.nan

                    sid = pu.retrieve_sid("mdns")
                    iid = pu.retrieve_iid("mdns")

                    packet_dict["StatusType"] = pu.compute_status_type(sid, iid)
                    packet_dict["Payload"] = np.nan

                    master_dict[counter] = packet_dict
                    counter += 1

                else:
                    packet_dict["SourcePort"] = np.nan
                    packet_dict["DestinationPort"] = np.nan
                    packet_dict["SourceIP"] = np.nan
                    packet_dict["DestinationIP"] = np.nan

                    sid = pu.retrieve_sid("malicious")
                    iid = pu.retrieve_iid("malicious")

                    packet_dict["StatusType"] = pu.compute_status_type(sid, iid)
                    packet_dict["Payload"] = np.nan

                    master_dict[counter] = packet_dict
                    counter += 1

            capture.close()
            print("Packets processed: " + str(counter + 1))

            # Write the newly parsed file to the 01_pol_preprocessed directory
            new_csv_filename = str(os.path.splitext(the_file)[0]) + ".csv"
            new_csv_path = os.path.join(output_folder_path, new_csv_filename)

            master_df = pd.DataFrame.from_dict(master_dict, orient="index")
            master_df.to_csv(new_csv_path, index=False)


def main():
    start = time.time()
    preprocess()
    end = time.time()
    print("Preprocessing layer execution time: " + str(end - start))


if __name__ == "__main__":
    main()
