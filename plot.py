#!python
import os
import pol_utilities as pu
import matplotlib.pyplot as plt
import numpy as np
import math
import pandas as pd

params = {
    "backend": "ps",
    "axes.labelsize": 18,
    "font.size": 18,
    "legend.fontsize": 16,
    "xtick.labelsize": 16,
    "ytick.labelsize": 16,
    "text.usetex": True,
}

plt.rcParams.update(params)


def plot_total_throughputs(input_folder_path, output_folder_path, file_list):
    for the_file in file_list:
        input_file_path = os.path.join(input_folder_path, the_file)
        df = pd.read_csv(input_file_path)
        print("Keane")
        x = df["Average_Timestamp"]
        y = df["TP_Overall"]

        fig, ax = plt.subplots(figsize=(10, 6))
        plt.plot(x, y)
        plt.xlabel("Time (s)")
        plt.ylabel("Total throughput (Bytes/sec)")

        output_file_name = "fig1.eps"
        output_file_path = os.path.join(output_folder_path, output_file_name)
        plt.tight_layout()
        plt.savefig(output_file_path, format="eps")

        plt.show()


def main():
    # Define input and output folder paths
    cwd = os.getcwd()
    input_folder_path = os.path.join(cwd, pu.root.get("feature_test"))
    output_folder_path = os.path.join(cwd, pu.root.get("profile"))

    # Files containing features (02_features)
    files_to_process = [
        f
        for f in os.listdir(input_folder_path)
        if os.path.isfile(os.path.join(input_folder_path, f))
        if f.endswith(".csv")
    ]

    # Plotting functions, comment out as required
    plot_total_throughputs(input_folder_path, output_folder_path, files_to_process)


if __name__ == "__main__":
    main()
