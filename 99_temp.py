import pandas as pd
import pol_utilities as pu
import os
import datetime as dt
import pyshark as ps


cwd = os.getcwd()

input_folder_path = pu.root.get("feature_test")
input_folder_path = os.path.join(cwd, input_folder_path)


files_to_process = [
    f
    for f in os.listdir(input_folder_path)
    if os.path.isfile(os.path.join(input_folder_path, f))
    if f.endswith(".csv")
]

for the_file in files_to_process:
    file_path = os.path.join(input_folder_path, the_file)
    df_master = pd.read_csv(file_path)
    print("Number of Nans in {} = {}".format(the_file, df_master.isnull().sum().sum()))


if False:
    filename = "CC_9-10.csv"

    path_01 = pu.root.get("preprocess")
    path_01 = os.path.join(cwd, path_01)
    path_01 = os.path.join(path_01, filename)

    path_11 = pu.root.get("preprocess_test")
    path_11 = os.path.join(cwd, path_11)
    path_11 = os.path.join(path_11, filename)

    df_01 = pd.read_csv(path_01)

    df_01_malicious = df_01[df_01["StatusType"] == "CRUISE"]
    print(df_01_malicious)

    df_11 = pd.read_csv(path_11)
    df_11_malicious = df_11[df_11["StatusType"] == "CRUISE"]
    print(df_11_malicious)
