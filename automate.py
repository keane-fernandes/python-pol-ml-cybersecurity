from py import test
import pandas as pd
import pol_utilities as pu
import os
import directories as dirs

cwd = os.getcwd()
print(cwd)

input_directories = {
    "raw": "00_pol_raw",
    "preprocessed": "01_pol_preprocessed",
    "training": "02_pol_training",
    "history": "03_pol_history",
    "profiles": "04_pol_profiles",
    "live": "99_pol_live",
}

theFolder = dirs.directories.get("raw")
directories = [dI for dI in os.listdir(cwd) if os.path.isdir(os.path.join(cwd, dI))]

listOfFiles = os.listdir(os.path.join(cwd, theFolder))

listOfFiles = [fi for fi in listOfFiles if fi.endswith(".pcapng")]


raw_directory = input_directories.get("raw")

print(raw_directory)

for dI in os.listdir(cwd):
    if os.path.isdir(os.path.join(cwd, dI)):
        print(cwd + os.path.sep + dI)
