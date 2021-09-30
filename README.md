# Introduction
This repository contains all of the scripts required to get you started with the Automotive Rig 1.0 from Thales.
# Setup
Prerequisite software:
1. Ensure you have [Wireshark](https://www.wireshark.org) installed.
2. Ensure that you [tshark](https://tshark.dev/setup/install/) installed.
3. Ensure that you have [Python](https://www.python.org) installed.

# Directories
1. [`00_raw`](./00_raw) - contains capture files from tshark in `.pcapng` format

# Scripts
1. [`attack.py`](./attack.py) -- the script used to perform a DoS attack on the hardware demonstrator. To perform this attack, the user needs to first connect a device to a free port on the switch, and then invoke the script from the terminal using a python interpreter.
`python3 attack.py`

2. [`collect.py`](./attack.py) -- reads in packet information from a .pcapng that has been captured by tshark, and outputs a CSV containing a list of pack
3. [`feature.py`](./feature.py) - 
4. [`plot.py`](./plot.py)
5. [`automate.py`](./automate.py)
6. [`testing.py`](./test.py)
7. [`train.py`](./train.py)
8. [`pol_utilities.py`](./pol_utilities.py)

# Datasets

# Usage
A simple workflow to extract features from the hardware demonstrator:
1. Capture packets using 