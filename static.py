import pyshark
import collections
import matplotlib.pyplot as plt
import numpy as np
import pol_utilities as pu

# Packet lists based on PolPacket class in pol_utilities
masterPacketList = []
vehicleSpeedPackets = []
throttlePedalPackets = []
brakeStatusPackets = []
cruiseControlPackets = []
broadcastPackets = []
maliciousPackets = []

# Behaviour Parameters
validPackets = 0
broadcastPackets = 0
maliciousPackets = 0
time = 0.0

# Import packets from capture file
capture = pyshark.FileCapture(
    "./pcaps/test.pcapng", only_summaries=False, keep_packets=False
)

# Iterate though packets and populate PolPacket object
for packet in capture:
    packet_length = packet.frame_info.len

    if pu.check_for_valid(packet):
        hexdump = packet.data.data
        status_type = pu.compute_status_type(packet)
        time_relative = packet.udp.time_relative
        time_delta = packet.udp.time_delta
        total_length = packet_length
        udp_length = packet.udp.length
        source_port = packet.udp.srcport
        destination_port = packet.udp.dstport
        source_ip = packet.ip.src
        destination_ip = packet.ip.dst
        keane = packet.data.ip
        sid = "1234556"
        iid = "1234060"

        # IP layer data extraction

        # Ethernet layer data extraction

        new_pol_pkt = pu.PolPacket(
            hexdump,
            status_type,
            time_relative,
            time_delta,
            total_length,
            source_port,
            destination_port,
            sid,
            iid,
            source_ip,
            destination_ip,
        )

        masterPacketList.append(new_pol_pkt)
        pu.PolPacket.increment_packet_counter()

    elif pu.check_for_broadcast(packet):
        pu.PolPacket.increment_packet_counter()
        pass
    else:
        pu.PolPacket.increment_packet_counter()
        pass

print("Total Packets: " + str(pu.PolPacket.counter))
print(hasattr(packet.udp, "payload"))

# Plot our results
if False:
    for pkt in masterPacketList:
        print(pkt.time_delta)

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
