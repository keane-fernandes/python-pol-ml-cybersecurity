#!python
import os
import pol_utilities as pu
import matplotlib.pyplot as plt
import numpy as np
import math
import pandas as pd

params = {
    "backend": "ps",
    "axes.labelsize": 12,
    "font.size": 12,
    "legend.fontsize": 10,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "text.usetex": True,
}

plt.rcParams.update(params)


def plot_throughputs(input_folder_path, output_folder_path, file_list):
    for the_file in file_list:
        input_file_path = os.path.join(input_folder_path, the_file)
        df = pd.read_csv(input_file_path)
        x = df["Average_Timestamp"]
        y1 = df["TP_Overall"]
        y2 = df["TP_Speed"]
        y3 = df["TP_Throttle"]
        y4 = df["TP_Brake"]
        y5 = df["TP_Cruise"]
        y6 = df["TP_Malicious"]

        fig, (ax1, ax2, ax3, ax4, ax5, ax6) = plt.subplots(
            6, 1, figsize=(10, 10), sharex=True
        )

        ax1.plot(x, y1, c="c", label="Network")
        ax1.legend(loc="upper right")

        ax2.plot(x, y2, c="g", label="Speed")
        ax2.legend(loc="upper right")

        ax3.plot(x, y3, c="b", label="Throttle")
        ax3.set_ylabel("Throughput (Bytes/second)")
        ax3.legend(loc="upper right")

        ax4.plot(x, y4, c="m", label="Brake")
        ax4.legend(loc="upper right")

        ax5.plot(x, y5, c="y", label="Cruise")
        ax5.legend(loc="upper right")

        ax6.plot(x, y6, c="r", label="Malicious")
        ax6.legend(loc="upper right")

        plt.xlabel("Time (s)")
        plt.tight_layout()

        output_file_name_eps = str(os.path.splitext(the_file)[0]) + "_throughputs.eps"
        output_file_name_png = str(os.path.splitext(the_file)[0]) + "_throughputs.png"

        output_file_path_eps = os.path.join(output_folder_path, output_file_name_eps)
        output_file_path_png = os.path.join(output_folder_path, output_file_name_png)

        plt.savefig(output_file_path_eps, format="eps")
        plt.savefig(output_file_path_png, format="png")

        if False:
            output_file_path = os.path.join(output_folder_path, output_file_name)
            plt.tight_layout()
            plt.savefig(output_file_path, format="eps")

            plt.show()


def main():
    # Define input and output folder paths
    cwd = os.getcwd()
    input_folder_path = os.path.join(cwd, pu.root.get("feature"))
    output_folder_path = os.path.join(cwd, pu.root.get("plot"))

    # Files containing features (02_features)
    files_to_process = [
        f
        for f in os.listdir(input_folder_path)
        if os.path.isfile(os.path.join(input_folder_path, f))
        if f.endswith(".csv")
    ]

    # Plotting functions, comment out as required
    plot_throughputs(input_folder_path, output_folder_path, files_to_process)


if __name__ == "__main__":
    main()
