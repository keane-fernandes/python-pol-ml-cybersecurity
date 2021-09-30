import numpy as np
import pandas as pd
import pyshark as ps
import pol_utilities as pu
import os

cwd = os.getcwd()
folder_path = os.path.join(cwd, pu.root.get("train"))

# Populates a nested dictionary of sniffed packets
def create_packet_dict(packet, packet_dict):
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

    elif pu.check_for_rrcp(packet):
        sid = pu.retrieve_sid("rrcp")
        iid = pu.retrieve_iid("rrcp")

        # Irrelevant, but kept in for dataframe uniformity
        packet_dict["SourcePort"] = np.nan
        packet_dict["DestinationPort"] = np.nan
        packet_dict["SourceIP"] = np.nan
        packet_dict["DestinationIP"] = np.nan

        packet_dict["StatusType"] = pu.compute_status_type(sid, iid)
        packet_dict["Payload"] = np.nan

    elif pu.check_for_dhcp(packet):
        packet_dict["SourcePort"] = int(packet.udp.srcport)
        packet_dict["DestinationPort"] = int(packet.udp.dstport)
        packet_dict["SourceIP"] = np.nan
        packet_dict["DestinationIP"] = np.nan

        sid = pu.retrieve_sid("dhcp")
        iid = pu.retrieve_iid("dhcp")

        packet_dict["StatusType"] = pu.compute_status_type(sid, iid)
        packet_dict["Payload"] = np.nan

    elif pu.check_for_ssdp(packet):
        packet_dict["SourcePort"] = int(packet.udp.srcport)
        packet_dict["DestinationPort"] = int(packet.udp.dstport)
        packet_dict["SourceIP"] = str(packet.ip.src)
        packet_dict["DestinationIP"] = str(packet.ip.dst)

        sid = pu.retrieve_sid("ssdp")
        iid = pu.retrieve_iid("ssdp")

        packet_dict["StatusType"] = pu.compute_status_type(sid, iid)
        packet_dict["Payload"] = np.nan

    elif pu.check_for_mdns(packet):
        packet_dict["SourcePort"] = int(packet.udp.srcport)
        packet_dict["DestinationPort"] = int(packet.udp.dstport)
        packet_dict["SourceIP"] = np.nan
        packet_dict["DestinationIP"] = np.nan

        sid = pu.retrieve_sid("mdns")
        iid = pu.retrieve_iid("mdns")

        packet_dict["StatusType"] = pu.compute_status_type(sid, iid)
        packet_dict["Payload"] = np.nan

    elif pu.check_for_arp(packet):
        packet_dict["SourcePort"] = np.nan
        packet_dict["DestinationPort"] = np.nan
        packet_dict["SourceIP"] = np.nan
        packet_dict["DestinationIP"] = np.nan

        sid = pu.retrieve_sid("arp")
        iid = pu.retrieve_iid("arp")

        packet_dict["StatusType"] = pu.compute_status_type(sid, iid)
        packet_dict["Payload"] = np.nan

    elif pu.check_for_nbns(packet):
        packet_dict["SourcePort"] = np.nan
        packet_dict["DestinationPort"] = np.nan
        packet_dict["SourceIP"] = np.nan
        packet_dict["DestinationIP"] = np.nan

        sid = pu.retrieve_sid("nbns")
        iid = pu.retrieve_iid("nbns")

        packet_dict["StatusType"] = pu.compute_status_type(sid, iid)
        packet_dict["Payload"] = np.nan

    elif pu.check_for_llmnr(packet):
        packet_dict["SourcePort"] = np.nan
        packet_dict["DestinationPort"] = np.nan
        packet_dict["SourceIP"] = np.nan
        packet_dict["DestinationIP"] = np.nan

        sid = pu.retrieve_sid("llmnr")
        iid = pu.retrieve_iid("llmnr")

        packet_dict["StatusType"] = pu.compute_status_type(sid, iid)
        packet_dict["Payload"] = np.nan

    elif pu.check_for_malformed(packet):
        packet_dict["SourcePort"] = np.nan
        packet_dict["DestinationPort"] = np.nan
        packet_dict["SourceIP"] = np.nan
        packet_dict["DestinationIP"] = np.nan

        sid = pu.retrieve_sid("malformed")
        iid = pu.retrieve_iid("malformed")

        packet_dict["StatusType"] = pu.compute_status_type(sid, iid)
        packet_dict["Payload"] = np.nan

    else:
        packet_dict["SourcePort"] = np.nan
        packet_dict["DestinationPort"] = np.nan
        packet_dict["SourceIP"] = np.nan
        packet_dict["DestinationIP"] = np.nan

        sid = pu.retrieve_sid("malicious")
        iid = pu.retrieve_iid("malicious")

        packet_dict["StatusType"] = pu.compute_status_type(sid, iid)
        packet_dict["Payload"] = np.nan


# Returns a aggregated dict of features from a chunk of packets
def create_feature_dict(df_packet, dict_feature):
    # Subtract the last timestamp from the first timestamp
    start_time = df_packet.iloc[0]["Timestamp"]
    end_time = df_packet.iloc[-1]["Timestamp"]

    time_window = end_time - start_time
    dict_feature = {}

    # Timeframe
    dict_feature["TimeWindow"] = time_window

    # Average timestamp for df_packet
    dict_feature["Average_Timestamp"] = (
        df_packet.iloc[-1]["Timestamp"] + df_packet.iloc[0]["Timestamp"]
    ) / 2

    # Separate master dataframe into smaller, signal specific dataframes
    df_speed = df_packet[df_packet["StatusType"] == "SPEED"]
    df_throttle = df_packet[df_packet["StatusType"] == "THROTTLE"]
    df_brake = df_packet[df_packet["StatusType"] == "BRAKE"]
    df_cruise = df_packet[df_packet["StatusType"] == "CRUISE"]
    df_rrcp = df_packet[df_packet["StatusType"] == "RRCP"]
    df_dhcp = df_packet[df_packet["StatusType"] == "DHCP"]
    df_mdns = df_packet[df_packet["StatusType"] == "MDNS"]
    df_ssdp = df_packet[df_packet["StatusType"] == "SSDP"]
    df_arp = df_packet[df_packet["StatusType"] == "ARP"]
    df_nbns = df_packet[df_packet["StatusType"] == "NBNS"]
    df_llmnr = df_packet[df_packet["StatusType"] == "LLMNR"]
    df_malformed = df_packet[df_packet["StatusType"] == "MALFORMED"]
    df_malicious = df_packet[df_packet["StatusType"] == "MALICIOUS"]

    # Throughputs
    dict_feature["TP_Overall"] = df_packet["PacketLength"].sum() / time_window
    dict_feature["TP_Speed"] = df_speed["PacketLength"].sum() / time_window
    dict_feature["TP_Throttle"] = df_throttle["PacketLength"].sum() / time_window
    dict_feature["TP_Brake"] = df_brake["PacketLength"].sum() / time_window
    dict_feature["TP_Cruise"] = df_cruise["PacketLength"].sum() / time_window
    dict_feature["TP_RRCP"] = df_rrcp["PacketLength"].sum() / time_window
    dict_feature["TP_DHCP"] = df_dhcp["PacketLength"].sum() / time_window
    dict_feature["TP_MDNS"] = df_mdns["PacketLength"].sum() / time_window
    dict_feature["TP_SSDP"] = df_ssdp["PacketLength"].sum() / time_window
    dict_feature["TP_Malicious"] = df_malicious["PacketLength"].sum() / time_window
    dict_feature["TP_ARP"] = df_arp["PacketLength"].sum() / time_window
    dict_feature["TP_NBNS"] = df_nbns["PacketLength"].sum() / time_window
    dict_feature["TP_LLMNR"] = df_llmnr["PacketLength"].sum() / time_window
    dict_feature["TP_Malformed"] = df_malformed["PacketLength"].sum() / time_window

    # Average payloads of vehicle speed, throttle, brake and cruise control

    dict_feature["VehicleSpeed"] = df_speed["Payload"].mean()
    dict_feature["ThrottleDemand"] = df_throttle["Payload"].mean()
    dict_feature["BrakePressed"] = df_brake["Payload"].mean()
    dict_feature["CruiseDemand"] = df_cruise["Payload"].mean()

    # Behaviour
    dict_feature["Behaviour"] = pu.get_behaviour(
        dict_feature["VehicleSpeed"], dict_feature["CruiseDemand"]
    )


# Sniffs on an interface
def sniff_packets(capture_dict):
    # The interface might be different for different devices
    capture = ps.LiveCapture(interface="en5", only_summaries=False)
    counter = 0

    # Instead of packet count, can insert a timeout instead
    for packet in capture.sniff_continuously(packet_count=179):
        packet_dict = {}
        create_packet_dict(packet, packet_dict)
        capture_dict[counter] = packet_dict
        counter += 1

    capture.close()


def main():
    # Continuously monitoring system, basis for machine learning
    while True:
        capture_dict = {}
        feature_dict = {}
        # Sniffs on the interface specified and populates the capture dictionary
        sniff_packets(capture_dict)
        # Create a dataframe of packets sniffed from this dictionary
        df_packet = pd.DataFrame.from_dict(capture_dict, orient="index")
        # Creates a feature vector from the captured packet block, use this as input
        # to classifier
        create_feature_dict(df_packet, feature_dict)
        # Do something with the feature vector for your application


if __name__ == "__main__":
    main()
