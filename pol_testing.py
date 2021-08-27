""""

This is a python script that performs assert tests and unit tests on
the methods in pol_utilities.py. This runs when setup.py runs.

"""
import pyshark as ps
import pol_utilities as pu

# Assert testing

string = '"Aug 20, 2021 19:30:34.106134000 BST"'
date = pu.extract_date(string)
time = pu.extract_time(string)
location = pu.extract_location(string)

assert date == "Aug-20-2021"
assert time == "19:30:34.106134000"
assert location == "BST"

# Unit tests
# Use the small pcap files in 05_pol_testing

if False:
    columns = ["Name", "Age"]

    df_master = pd.read_csv("./live.csv")
    df_master.to_csv("./another_output.csv", index=False)
