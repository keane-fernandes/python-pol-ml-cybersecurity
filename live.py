import pyshark
import plot

# This is a python utility to capture packets live over the
# Automotive Rig v1.0 from Thales.

# Interface might need to be changed depending on your system.
capture = pyshark.LiveCapture(
    interface="en5", only_summaries=False, display_filter="udp"
)

for packet in capture.sniff_continuously(packet_count=1):
    if False:
        # Prints out packet as a string -- change only_summaries
        # to True if you want one line
        print(packet.__str__())
        #
        print(packet.frame_info)
        # Check for fields in packet that can be accessed
        attributes = dir(packet)
        print(attributes)
        # Print highest layer
        if packet.highest_layer != "DATA":
            print("Anomaly detected")

    print(packet.get_multiple_layers)


capture.close()
