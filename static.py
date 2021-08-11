import pyshark
import collections
import matplotlib.pyplot as plt
import numpy as np

# Import packets from capture file (Change this to accept command
# line arguments, basically make it more flexible)


def is_not_blank(s):
    return bool(s and not s.isspace())


capture = pyshark.FileCapture("./pcaps/test.pcapng", only_summaries=False)

# Create attribute lists
indices = []
timestamps = []
source = []
destination = []
protocolList = []
packetLength = []
throttlePedalDemand = []
brakeStatus = []

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
    packetLength.append(formattedLine[5])
    throttlePedalDemand.append(formattedLine[6])
    brakeStatus.append(formattedLine[7])

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

print("Number of packets processed: " + str(numberOfPackets))
print("Size of formatted line list: " + str(len(formattedLine)))
print("Number of timestamps processed: " + str(len(timestamps)))
print("Number of sources processed: " + str(len(source)))
print("Number of destinations processed: " + str(len(destination)))
print("Number of protocols processed: " + str(len(protocolList)))
print("Number of lengths processed: " + str(len(packetLength)))

if False:
    print(capture[0].data.data)
    print(capture[1].data.data)
    print(capture[2].data.data)
    print(capture[3].data.data)
    print(capture[4].data.data)
    print(capture[5].data.data)
    print(capture[6].data.data)
