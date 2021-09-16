import numpy as np
import pandas as pd
from pandas.core.indexes.base import Index
import pyshark as ps
import pol_utilities as pu
import os

cwd = os.getcwd()
folder_path = os.path.join(cwd, pu.root.get("train"))
processing_folder_path = os.path.join(folder_path, "attack")

files_to_process = [
    f
    for f in os.listdir(processing_folder_path)
    if os.path.isfile(os.path.join(processing_folder_path, f))
    if f.endswith(".csv")
]

dataset_attack_master = pd.DataFrame

frames = []

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

    dataset_training = dataset[
        [
            "TP_Overall",
            "TP_Speed",
            "TP_Brake",
            "TP_Cruise",
            "TP_RRCP",
            "TP_Malicious",
            "TP_ARP",
            "VehicleSpeed",
            "ThrottleDemand",
            "BrakePressed",
            "CruiseDemand",
            "Attack",
        ]
    ]

    frames.append(dataset_training)

    # output_file_path = os.path.join(folder_path, "attack_master_training.csv")
    # dataset_training.to_csv(output_file_path, index=False)

result = pd.concat(frames)

output_file_path = os.path.join(folder_path, "attack_master_training.csv")
result.to_csv(output_file_path, index=False)

# print(df_arp[["TP_ARP"]])
# print(df_malicious[["TP_Malicious"]])
