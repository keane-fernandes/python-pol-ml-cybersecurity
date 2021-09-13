import pandas as pd
import pyshark as ps
import pol_utilities as pu
import os

cwd = os.getcwd()
input_folder_path = os.path.join(cwd, pu.root.get("input"))
output_folder_path = os.path.join(cwd, pu.root.get("output"))
