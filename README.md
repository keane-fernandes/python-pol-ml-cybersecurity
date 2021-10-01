# Introduction
This repository contains all of the scripts required to get you started with the Automotive Rig 1.0 from Thales.
# Setup
1. Ensure you have [Wireshark](https://www.wireshark.org) installed.
2. Ensure that you [tshark](https://tshark.dev/setup/install/) installed.
3. Ensure that you have [Python](https://www.python.org) installed.
4. Set up a virtual environment using [venv](https://virtualenv.pypa.io/en/latest/) and install the required dependencies using the provided [requirements.txt](./requirements.txt).

# Directories
## Training

1. [`00_raw`](./00_raw) - contains capture files from tshark in `.pcapng` format.
2. [`01_collect`](./01_collect) - information from the capture files from `00_raw` is cleaned and saved in this folder as a time series of packets as a CSV file.
3. [`02_feature`](./02_features) - information from the CSV files from `01_collect` is aggregated and saved as a time series of features in this folder as a CSV. Example features include network throughputs, vehicle speed, throttle demand, brake status, cruise control.
4. [`03_train`](./03_train) - contains the baseline data and attack data used for training the binary classifier.
5. [`05_plot`](./05_plots) - contains all of the plots of the colllected baseline and attack data.

## Validation
6. [`07_live_raw`](./07_live_raw) - contains the capture files of the DoS attacks performed at different rates (0.1s -0.5s)
7. [`08_live_collect`](./08_live_collect) - contains the cleaned capture files from `07_live_raw` as a CSV file.
8. [`09_live_features`](./09_live_features) - aggregated features of the files from `08_live_collect`.
9. [`10_live_throuhgputs`](./10_live_throughputs) - contains the throughputs (features) used to test the binary classifier.
10. [`11_live_plot`](./11_live_plot) - contains plots of network activity of validation set DoS attacks.

# Scripts
1. [`attack.py`](./attack.py) -- the script used to perform a DoS attack on the hardware demonstrator. To perform this attack, the user needs to first connect a device to a free port on the switch, set itself a static IP, and then invoke the script from the terminal using a python interpreter. An example would be: `python3 attack.py`
2. [`collect.py`](./collect.py) -- reads in packet information from a .pcapng that has been captured by tshark, and outputs a CSV containing a time series of sniffed packets.
3. [`feature.py`](./feature.py) - aggregates features from the time series of packets from `collect.py`, and outputs a CSV containing these features.
4. [`plot.py`](./plot.py) - plots the monitored network activity.
5. [`automate.py`](./automate.py) - automates the collect, feature and plot modules.
6. [`testing.py`](./test.py) - performs the unit tests, using the files stored in [`06_testing`](./06_testing)
7. [`train.py`](./train.py) - script used to evaluate the performance of the binary classifers on the training and testing sets.
8. [`pol_utilities.py`](./pol_utilities.py) - helper methods for all of the modules.