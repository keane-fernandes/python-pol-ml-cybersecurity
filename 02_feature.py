import os
import pol_utilities as pu
import pandas as pd
import matplotlib.pyplot as plt

cwd = os.getcwd()
input_folder_path = os.path.join(cwd, pu.root.get("temp"))

files_to_process = [
    f
    for f in os.listdir(input_folder_path)
    if os.path.isfile(os.path.join(input_folder_path, f))
    if f.endswith(".csv")
]

for f in files_to_process:
    file_path = os.path.join(input_folder_path, f)
    iter_csv = pd.read_csv(file_path, iterator=True, chunksize=1000)

    broadcast = pd.concat([chunk[chunk["StatusType"] == "B"] for chunk in iter_csv])

    broadcast["RollingMean"] = (
        broadcast["TimeDelta"].rolling(window=5, center=True).mean()
    )

    s = broadcast.xs("RollingMean", axis=1)
    plt.plot(s)
    plt.show()
