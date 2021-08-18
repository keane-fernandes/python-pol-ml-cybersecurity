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
    "./pcaps/test_with_broadcast.pcapng", only_summaries=False, keep_packets=False
)

# Iterate though packets and populate PolPacket object
for packet in capture:
    packet_length = packet.frame_info.len
    timestamp = packet.frame_info.time_relative
    time_delta = packet.frame_info.time_delta

    if pu.check_for_valid(packet):

        byte_field = packet.udp.payload.split(":")

        sid = pu.extract_sid(byte_field)
        iid = pu.extract_iid(byte_field)

        status_type = pu.compute_status_type(sid, iid)

        payload = pu.extract_payload(byte_field, status_type)

        # UDP Layer data extraction
        source_port = int(packet.udp.srcport)
        destination_port = int(packet.udp.dstport)

        # IP layer data extraction
        source_ip = str(packet.ip.src)
        destination_ip = str(packet.ip.dst)

        # Ethernet layer data extraction

        new_pol_pkt = pu.PolPacket(
            status_type,
            timestamp,
            time_delta,
            packet_length,
            source_ip,
            destination_ip,
            source_port,
            destination_port,
            payload,
        )

        masterPacketList.append(new_pol_pkt)
        pu.PolPacket.increment_packet_counter()

    elif pu.check_for_broadcast(packet):
        sid = pu.get_broadcast_sid()
        iid = pu.get_broadcast_iid()

        status_type = pu.compute_status_type(sid, iid)

        new_pol_pkt = pu.PolPacket(
            status_type,
            timestamp,
            time_delta,
        )
        masterPacketList.append(new_pol_pkt)

        pu.PolPacket.increment_packet_counter()

    # Another elif for DHCP / SSDP
    else:

        pu.PolPacket.increment_packet_counter()


for polpacket in masterPacketList:
    polpacket.print_summary()


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
