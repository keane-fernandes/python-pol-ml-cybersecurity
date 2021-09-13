import os
import pol_utilities as pu
import pandas as pd
import matplotlib.pyplot as plt
import time
import numpy as np


def feature(input_folder_key, output_folder_key):
    cwd = os.getcwd()
    input_folder_path = os.path.join(cwd, pu.root.get(input_folder_key))
    output_folder_path = os.path.join(cwd, pu.root.get(output_folder_key))

    files_to_process = [
        f
        for f in os.listdir(input_folder_path)
        if os.path.isfile(os.path.join(input_folder_path, f))
        if f.endswith(".csv")
    ]

    processed = [
        d
        for d in os.listdir(output_folder_path)
        if os.path.isfile(os.path.join(output_folder_path, d))
        if d.endswith(".csv")
    ]

    for the_file in files_to_process:
        if not pu.check_if_preprocessed(the_file, processed):
            print("Currently processing: {}".format(the_file))
            file_path = os.path.join(input_folder_path, the_file)
            df_master = pd.read_csv(file_path)

            master_dict = {}
            counter = 0

            # 23 is a prime number and should prevent any cyclic patterns
            number_of_chunks = round(df_master.shape[0] / pu.chunk_size)

            for chunk in np.array_split(df_master, number_of_chunks):

                # Subtract the last timestamp from the first timestamp
                start_time = chunk.iloc[0]["Timestamp"]
                end_time = chunk.iloc[-1]["Timestamp"]

                time_window = end_time - start_time
                features_dict = {}

                # Timeframe
                features_dict["TimeWindow"] = time_window

                # Average timestamp for chunk
                features_dict["Average_Timestamp"] = (
                    chunk.iloc[-1]["Timestamp"] + chunk.iloc[0]["Timestamp"]
                ) / 2

                # Separate master dataframe into smaller, signal specific dataframes
                df_speed = chunk[chunk["StatusType"] == "SPEED"]
                df_throttle = chunk[chunk["StatusType"] == "THROTTLE"]
                df_brake = chunk[chunk["StatusType"] == "BRAKE"]
                df_cruise = chunk[chunk["StatusType"] == "CRUISE"]
                df_rrcp = chunk[chunk["StatusType"] == "RRCP"]
                df_dhcp = chunk[chunk["StatusType"] == "DHCP"]
                df_mdns = chunk[chunk["StatusType"] == "MDNS"]
                df_ssdp = chunk[chunk["StatusType"] == "SSDP"]
                df_arp = chunk[chunk["StatusType"] == "ARP"]
                df_nbns = chunk[chunk["StatusType"] == "NBNS"]
                df_llmnr = chunk[chunk["StatusType"] == "LLMNR"]
                df_malformed = chunk[chunk["StatusType"] == "MALFORMED"]
                df_malicious = chunk[chunk["StatusType"] == "MALICIOUS"]

                # Throughputs

                features_dict["TP_Overall"] = chunk["PacketLength"].sum() / time_window
                features_dict["TP_Speed"] = df_speed["PacketLength"].sum() / time_window
                features_dict["TP_Throttle"] = (
                    df_throttle["PacketLength"].sum() / time_window
                )
                features_dict["TP_Brake"] = df_brake["PacketLength"].sum() / time_window
                features_dict["TP_Cruise"] = (
                    df_cruise["PacketLength"].sum() / time_window
                )
                features_dict["TP_RRCP"] = df_rrcp["PacketLength"].sum() / time_window
                features_dict["TP_DHCP"] = df_dhcp["PacketLength"].sum() / time_window
                features_dict["TP_MDNS"] = df_mdns["PacketLength"].sum() / time_window
                features_dict["TP_SSDP"] = df_ssdp["PacketLength"].sum() / time_window
                features_dict["TP_Malicious"] = (
                    df_malicious["PacketLength"].sum() / time_window
                )
                features_dict["TP_ARP"] = df_arp["PacketLength"].sum() / time_window
                features_dict["TP_NBNS"] = df_nbns["PacketLength"].sum() / time_window
                features_dict["TP_LLMNR"] = df_llmnr["PacketLength"].sum() / time_window
                features_dict["TP_MALFORMED"] = (
                    df_malformed["PacketLength"].sum() / time_window
                )

                # Average payloads of vehicle speed, throttle, brake and cruise control

                features_dict["VehicleSpeed"] = df_speed["Payload"].mean()
                features_dict["ThrottleDemand"] = df_throttle["Payload"].mean()
                features_dict["BrakePressed"] = df_brake["Payload"].mean()
                features_dict["CruiseDemand"] = df_cruise["Payload"].mean()

                # Behaviour
                features_dict["Behaviour"] = pu.get_behaviour(
                    features_dict["VehicleSpeed"], features_dict["CruiseDemand"]
                )

                # Add the populated features_dict to the master_dict with the counter as the key
                master_dict[counter] = features_dict

                counter += 1

            # Create our Dataframe from the nested dictionary and output to csv

            df_features = pd.DataFrame.from_dict(master_dict, orient="index")
            new_file_path = os.path.join(output_folder_path, str(the_file))
            df_features.to_csv(new_file_path, index=False)
            print("Dataset with {} rows generated.".format(df_features.shape[0]))


def main(input_folder_key="collect", output_folder_key="feature"):
    print("Feature extraction layer started ...")
    start = time.time()
    feature(input_folder_key, output_folder_key)
    end = time.time()
    print("Feature layer execution time: " + str(end - start))


if __name__ == "__main__":
    main()
