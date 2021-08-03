import pyshark
import collections
import matplotlib as plt
import numpy as np

capture = pyshark.FileCapture("./pcaps/baseline-1.pcapng", only_summaries=True)

print(capture[0])


if False:
    print("Packet Summary: \n")
    print(example_packet)
    print("Packet Length: " + example_packet.length + "\n")
