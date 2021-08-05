import pyshark
import collections
import matplotlib.pyplot as plt
import numpy as np

# Import packets from capture file
capture = pyshark.FileCapture("./pcaps/baseline-1.pcapng", only_summaries=True)
protocolList = []
numberOfPackets = 0
# Iterate though packets and create lists of each attribute
for packet in capture:
    numberOfPackets += 1
    line = str(packet)
    formattedLine = line.split(" ")
    protocolList.append(formattedLine[4])

counter = collections.Counter(protocolList)

# Plot our results
plt.style.use("ggplot")
y_pos = np.arange(len(list(counter.keys())))
plt.bar(
    y_pos, list(counter.values()), align="center", alpha=0.5, color=["b", "g", "r", "c"]
)
plt.xticks(y_pos, list(counter.keys()))
plt.ylabel("Frequency")
plt.show()

print(numberOfPackets)
