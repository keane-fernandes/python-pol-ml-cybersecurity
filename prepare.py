""""

This is a python utility to capture packets live over the Automotive Rig v1.0 from Thales.
The user needs to define only ONE of the following as an argument on the command line:

"""

import pyshark as ps
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import time
import pol_utilities as pu
import os
import feature
import collect
import plot


def prepare_no_CC_training():
    cwd = os.getcwd()
    folder_path = os.path.join(cwd, pu.root.get("train"))
    processing_folder_path = os.path.join(folder_path, "no_cruising")

    files_to_process = [
        f
        for f in os.listdir(processing_folder_path)
        if os.path.isfile(os.path.join(processing_folder_path, f))
        if f.endswith(".csv")
    ]

    frames = []
    time_windows = []

    for the_file in files_to_process:
        file_path = os.path.join(processing_folder_path, the_file)
        dataset = pd.read_csv(file_path)

        dataset["Attack"] = 0
        dataset["Attack"] = dataset["Attack"].astype(int)
        time_window = dataset["TimeWindow"].mean()
        time_windows.append(time_window)

        dataset_training = dataset[
            [
                "TP_Overall",
                "TP_Speed",
                "TP_Throttle",
                "TP_Brake",
                "TP_Cruise",
                "TP_RRCP",
                "TP_Malicious",
                "TP_ARP",
                "Attack",
            ]
        ]

        frames.append(dataset_training)

    # Output concatenated dataframe
    result = pd.concat(frames)
    average_time_window = sum(time_windows) / len(time_windows)
    print("Average Time Window (no CC) = " + str(average_time_window))
    output_file_path = os.path.join(folder_path, "no_CC_training.csv")
    result.to_csv(output_file_path, index=False)


def prepare_CC_training():
    cwd = os.getcwd()
    folder_path = os.path.join(cwd, pu.root.get("train"))
    processing_folder_path = os.path.join(folder_path, "cruising")

    files_to_process = [
        f
        for f in os.listdir(processing_folder_path)
        if os.path.isfile(os.path.join(processing_folder_path, f))
        if f.endswith(".csv")
    ]

    frames = []
    time_windows = []

    for the_file in files_to_process:
        file_path = os.path.join(processing_folder_path, the_file)
        dataset = pd.read_csv(file_path)

        dataset["Attack"] = 0
        dataset["Attack"] = dataset["Attack"].astype(int)
        time_window = dataset["TimeWindow"].mean()
        time_windows.append(time_window)

        dataset_training = dataset[
            [
                "TP_Overall",
                "TP_Speed",
                "TP_Throttle",
                "TP_Brake",
                "TP_Cruise",
                "TP_RRCP",
                "TP_Malicious",
                "TP_ARP",
                "Attack",
            ]
        ]

        frames.append(dataset_training)

    # Output concatenated dataframe
    result = pd.concat(frames)
    average_time_window = sum(time_windows) / len(time_windows)
    print("Average Time Window (CC) = " + str(average_time_window))
    output_file_path = os.path.join(folder_path, "CC_training.csv")
    result.to_csv(output_file_path, index=False)


def prepare_attack_training():
    cwd = os.getcwd()
    folder_path = os.path.join(cwd, pu.root.get("train"))
    processing_folder_path = os.path.join(folder_path, "attack")

    files_to_process = [
        f
        for f in os.listdir(processing_folder_path)
        if os.path.isfile(os.path.join(processing_folder_path, f))
        if f.endswith(".csv")
    ]

    frames = []
    time_windows = []

    for the_file in files_to_process:
        file_path = os.path.join(processing_folder_path, the_file)
        dataset = pd.read_csv(file_path)

        arp_start = dataset[dataset["TP_ARP"] != 0].head(1).index.values[0]
        malicious_start = dataset[dataset["TP_Malicious"] != 0].head(1).index.values[0]

        attack_index = arp_start

        if malicious_start < arp_start:
            attack_index = malicious_start

        dataset.loc[dataset.index < attack_index, "Attack"] = 0
        dataset.loc[dataset.index >= attack_index, "Attack"] = 1

        dataset["Attack"] = dataset["Attack"].astype(int)
        time_window = dataset["TimeWindow"].mean()
        time_windows.append(time_window)

        dataset_training = dataset[
            [
                "TP_Overall",
                "TP_Speed",
                "TP_Throttle",
                "TP_Brake",
                "TP_Cruise",
                "TP_RRCP",
                "TP_Malicious",
                "TP_ARP",
                "Attack",
            ]
        ]

        frames.append(dataset_training)

    # Output concatenated dataframe
    result = pd.concat(frames)
    average_time_window = sum(time_windows) / len(time_windows)
    print("Average Time Window (Attack) = " + str(average_time_window))
    output_file_path = os.path.join(folder_path, "attack_training.csv")
    result.to_csv(output_file_path, index=False)


def prepare_attack_testing():
    cwd = os.getcwd()
    input_folder_path = os.path.join(cwd, pu.root.get("live_feature"))

    files_to_process = [
        f
        for f in os.listdir(input_folder_path)
        if os.path.isfile(os.path.join(input_folder_path, f))
        if f.endswith(".csv")
    ]

    frames = []

    for the_file in files_to_process:
        file_path = os.path.join(input_folder_path, the_file)
        dataset = pd.read_csv(file_path)

        arp_start = dataset[dataset["TP_ARP"] != 0].head(1).index.values[0]
        malicious_start = dataset[dataset["TP_Malicious"] != 0].head(1).index.values[0]

        attack_index = arp_start

        if malicious_start < arp_start:
            attack_index = malicious_start

        dataset.loc[dataset.index < attack_index, "Attack"] = 0
        dataset.loc[dataset.index >= attack_index, "Attack"] = 1

        dataset["Attack"] = dataset["Attack"].astype(int)

        dataset_training = dataset[
            [
                "TP_Overall",
                "TP_Speed",
                "TP_Throttle",
                "TP_Brake",
                "TP_Cruise",
                "TP_RRCP",
                "TP_Malicious",
                "TP_ARP",
                "Attack",
            ]
        ]

        frames.append(dataset_training)

    # Output concatenated dataframe
    result = pd.concat(frames)
    output_file_path = os.path.join(pu.root.get("live_throughput"), "TESTING.csv")
    result.to_csv(output_file_path, index=False)


def merge_training_and_baseline():
    cwd = os.getcwd()
    input_folder_path = os.path.join(cwd, pu.root.get("train"))

    files_to_process = ["attack_training.csv", "CC_training.csv", "no_CC_training.csv"]

    frames = []

    for the_file in files_to_process:
        file_path = os.path.join(input_folder_path, the_file)
        dataset = pd.read_csv(file_path)
        frames.append(dataset)

    training_data = pd.concat(frames)

    output_file_path = os.path.join(input_folder_path, "TRAINING.csv")
    training_data.to_csv(output_file_path, index=False)


if __name__ == "__main__":
    if False:
        prepare_no_CC_training()
        prepare_CC_training()
        prepare_attack_training()
        merge_training_and_baseline()
    prepare_attack_testing()
