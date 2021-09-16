import numpy as np
import pandas as pd
import pyshark as ps
import pol_utilities as pu
import os

TP_Overall_min = 0
TP_Overall_max = 0

TP_Speed_min = 0
TP_Speed_max = 0

TP_Brake_min = 0
TP_Brake_max = 0

TP_throttle_min = 0
TP_throttle_max = 0

TP_cruise_min = 0
TP_cruise_max = 0

TP_RRCP_min = 0
TP_RRCP_max = 0

TP_ARP_min = 0
TP_ARP_max = 0

TP_Malicious_min = 0
TP_Malicious_max = 0

cwd = os.getcwd()
folder_path = os.path.join(cwd, pu.root.get("train"))

files_to_process = ["CC_master_training.csv", "no_CC_master_training.csv"]

for the_file in files_to_process:
    file_path = os.path.join(folder_path, the_file)
    dataset = pd.read_csv(file_path)
    print(dataset["TP_Overall"].max())
    print(dataset["TP_Overall"].min())


# print(df_arp[["TP_ARP"]])
# print(df_malicious[["TP_Malicious"]])
