import pyshark
import collections
import matplotlib.pyplot as plt
import numpy as np

# Import packets from capture file (Change this to accept command
# line arguments, basically make it more flexible)
capture = pyshark.FileCapture("./pcaps/baseline-1.pcapng", only_summaries=True)

# Create attribute lists
indices = []
timestamps = []
source = []
destination = []
protocolList = []
packetLength = []

numberOfPackets = 0

# Iterate though packets and populate attribute lists
for packet in capture:
    numberOfPackets += 1
    line = str(packet)
    formattedLine = line.split(" ")
    indices.append(formattedLine[0])
    timestamps.append(formattedLine[1])
    source.append(formattedLine[2])
    destination.append(formattedLine[3])
    protocolList.append(formattedLine[4])

counter = collections.Counter(protocolList)

# Real-time sniffing of packets
# Specify interface to sniff on


# Plot our results
if False:
    plt.style.use("ggplot")
    y_pos = np.arange(len(list(counter.keys())))
    plt.bar(
        y_pos,
        list(counter.values()),
        align="center",
        alpha=0.5,
        color=["b", "g", "r", "c"],
    )
    plt.xticks(y_pos, list(counter.keys()))
    plt.ylabel("Frequency")
    plt.show()

print('Number of packets processed: ' + numberOfPackets)
print('Number of indices processed: ' + numberOfPackets)
print('Number of packets processed: ' + numberOfPackets)
print('Number of packets processed: ' + numberOfPackets)
print('Number of packets processed: ' + numberOfPackets)