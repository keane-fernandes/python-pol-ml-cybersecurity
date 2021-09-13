#!python
import os
import pol_utilities as pu
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import math
import pandas as pd


def plot_throughputs(input_folder_path, output_folder_path, file_list):
    params = {
        "backend": "ps",
        "axes.labelsize": 20,
        "font.size": 12,
        "legend.fontsize": 10,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "text.usetex": True,
    }

    plt.rcParams.update(params)

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
        y7 = df["TP_RRCP"]
        y8 = df["TP_ARP"]
        y9 = df["TP_NBNS"]
        y10 = df["TP_LLMNR"]
        y11 = df["TP_Malformed"]

        fig, (ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9, ax10, ax11) = plt.subplots(
            11, 1, figsize=(10, 14), sharex=True
        )

        ax1.plot(x, y1, c="c", label="Network")
        ax1.set_ylim(bottom=0)
        ax1.legend(loc="upper right")

        ax2.plot(x, y2, c="g", label="Speed")
        ax2.set_ylim(bottom=0)
        ax2.legend(loc="upper right")

        ax3.plot(x, y3, c="b", label="Throttle")
        ax3.set_ylim(bottom=0)
        ax3.legend(loc="upper right")

        ax4.plot(x, y4, c="m", label="Brake")
        ax4.set_ylim(bottom=0)
        ax4.legend(loc="upper right")

        ax5.plot(x, y5, c="y", label="Cruise")
        ax5.set_ylim(bottom=0)
        ax5.set_ylabel("Throughput (Bytes/second)")
        ax5.legend(loc="upper right")

        ax6.plot(x, y6, c="r", label="Malicious")
        ax6.set_ylim(bottom=0)
        ax6.legend(loc="upper right")

        ax7.plot(x, y7, c="k", label="RRCP")
        ax7.set_ylim(bottom=0)
        ax7.legend(loc="upper right")

        ax8.plot(x, y8, c="c", label="ARP")
        ax8.set_ylim(bottom=0)
        ax8.legend(loc="upper right")

        ax9.plot(x, y9, c="g", label="NBNS")
        ax9.set_ylim(bottom=0)
        ax9.legend(loc="upper right")

        ax10.plot(x, y10, c="b", label="LLMNR")
        ax10.set_ylim(bottom=0)
        ax10.legend(loc="upper right")

        ax11.plot(x, y11, c="m", label="Malformed")
        ax11.set_ylim(bottom=0)
        ax11.legend(loc="upper right")

        plt.xlabel("Time (s)")
        plt.tight_layout()

        output_file_name_eps = str(os.path.splitext(the_file)[0]) + "_throughputs.eps"
        output_file_name_png = str(os.path.splitext(the_file)[0]) + "_throughputs.png"

        output_file_path_eps = os.path.join(output_folder_path, output_file_name_eps)
        output_file_path_png = os.path.join(output_folder_path, output_file_name_png)

        plt.savefig(output_file_path_eps, format="eps")
        plt.savefig(output_file_path_png, format="png")

        plt.close(fig)

        if False:
            output_file_path = os.path.join(output_folder_path, output_file_name)
            plt.tight_layout()
            plt.savefig(output_file_path, format="eps")

            plt.show()


def plot_benchmarks():
    params = {
        "backend": "ps",
        "axes.labelsize": 22,
        "font.size": 22,
        "legend.fontsize": 20,
        "xtick.labelsize": 20,
        "ytick.labelsize": 20,
        "text.usetex": True,
    }

    plt.rcParams.update(params)

    x = [100, 1000, 10000, 100000, 200000]
    lists = [1.13234, 3.43259, 49.84063, 649.81342, 1241.81342]
    dicts = [0.81924, 2.70842, 41.73492, 121.95863, 244.59186]

    fig, ax = plt.subplots(1, 1, figsize=(7, 7))

    ax.plot(x, lists, label="Approach 2 - List")
    ax.plot(x, dicts, label="Approach 3 - Dict")
    ax.set_xlabel("Number of Packets")
    ax.set_ylabel("Execution Time (s)")
    plt.ticklabel_format(style="sci", axis="x", scilimits=(0, 2))
    plt.ticklabel_format(style="sci", axis="y", scilimits=(0, 2))
    ax.legend(loc="upper left")

    filepath = "./benchmarks.eps"

    plt.savefig(filepath, format="eps")


def main(input_folder_key="feature", output_folder_key="plot"):
    print("Processing plots ...")
    # Define input and output folder paths
    cwd = os.getcwd()
    input_folder_path = os.path.join(cwd, pu.root.get(input_folder_key))
    output_folder_path = os.path.join(cwd, pu.root.get(output_folder_key))

    # Files containing features (02_features)
    files_to_process = [
        f
        for f in os.listdir(input_folder_path)
        if os.path.isfile(os.path.join(input_folder_path, f))
        if f.endswith(".csv")
    ]

    # Plotting functions, comment out as required
    plot_throughputs(input_folder_path, output_folder_path, files_to_process)
    # plot_benchmarks()
