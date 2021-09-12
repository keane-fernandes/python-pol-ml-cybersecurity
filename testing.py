""""

This is a python script that performs assert tests and unit tests on
the methods in pol_utilities.py. This runs when setup.py runs.

"""
import pyshark as ps
import pol_utilities as pu
import os
import unittest

cwd = os.getcwd()
test_directory = os.path.join(cwd, pu.root.get("testing"))


class UtilityChecks(unittest.TestCase):
    def test_extract_bytes(self):
        test_byte_field = ["ab", "cd", "ef"]
        self.assertEqual(pu.extract_bytes(test_byte_field, 0, 0), "")
        self.assertEqual(pu.extract_bytes(test_byte_field, 0, 1), "ab")
        self.assertEqual(pu.extract_bytes(test_byte_field, 0, 2), "abcd")
        self.assertEqual(pu.extract_bytes(test_byte_field, 100, 93), "")
        self.assertEqual(pu.extract_bytes(test_byte_field, 0, 0), "")

        test_byte_field = []
        self.assertEqual(pu.extract_bytes(test_byte_field, 0, 0), "")
        self.assertEqual(pu.extract_bytes(test_byte_field, 0, 1), "")
        self.assertEqual(pu.extract_bytes(test_byte_field, 0, 2), "")
        self.assertEqual(pu.extract_bytes(test_byte_field, 100, 93), "")
        self.assertEqual(pu.extract_bytes(test_byte_field, 0, 0), "")


class PacketChecks(unittest.TestCase):
    def test_speed(self):
        file_path = os.path.join(test_directory, "valid_speed.pcapng")
        capture = ps.FileCapture(file_path, only_summaries=False)
        packet = capture[0]
        self.assertTrue(pu.check_number_of_layers(packet, 4))
        self.assertTrue(pu.check_for_layers(packet, "eth", "ip", "data", "udp"))
        self.assertTrue(pu.check_for_valid(packet))
        capture.close()

    def test_throttle(self):
        file_path = os.path.join(test_directory, "valid_throttle.pcapng")
        capture = ps.FileCapture(file_path, only_summaries=False)
        packet = capture[0]
        self.assertTrue(pu.check_number_of_layers(packet, 4))
        self.assertTrue(pu.check_for_layers(packet, "eth", "ip", "data", "udp"))
        self.assertTrue(pu.check_for_valid(packet))
        capture.close()

    def test_brake(self):
        file_path = os.path.join(test_directory, "valid_brake.pcapng")
        capture = ps.FileCapture(file_path, only_summaries=False)
        packet = capture[0]
        self.assertTrue(pu.check_number_of_layers(packet, 4))
        self.assertTrue(pu.check_for_layers(packet, "eth", "ip", "data", "udp"))
        self.assertTrue(pu.check_for_valid(packet))
        capture.close()

    def test_cruise(self):
        file_path = os.path.join(test_directory, "valid_cruise.pcapng")
        capture = ps.FileCapture(file_path, only_summaries=False)
        packet = capture[0]
        self.assertTrue(pu.check_number_of_layers(packet, 4))
        self.assertTrue(pu.check_for_layers(packet, "eth", "ip", "data", "udp"))
        self.assertTrue(pu.check_for_valid(packet))
        capture.close()

    def test_broadcast(self):
        file_path = os.path.join(test_directory, "rrcp.pcapng")
        capture = ps.FileCapture(file_path, only_summaries=False)
        packet = capture[0]
        self.assertTrue(pu.check_for_broadcast(packet))
        capture.close()

    def test_dhcp(self):
        file_path = os.path.join(test_directory, "dhcp.pcapng")
        capture = ps.FileCapture(file_path, only_summaries=False)
        packet = capture[0]
        self.assertTrue(pu.check_number_of_layers(packet, 4))
        self.assertTrue(pu.check_for_layers(packet, "dhcp"))
        capture.close()

    def test_mdns(self):
        file_path = os.path.join(test_directory, "mdns.pcapng")
        capture = ps.FileCapture(file_path, only_summaries=False)
        packet = capture[0]
        self.assertTrue(pu.check_number_of_layers(packet, 4))
        self.assertTrue(pu.check_for_layers(packet, "mdns"))
        capture.close()

    def test_ssdp(self):
        file_path = os.path.join(test_directory, "ssdp.pcapng")
        capture = ps.FileCapture(file_path, only_summaries=False)
        packet = capture[0]
        self.assertTrue(pu.check_number_of_layers(packet, 4))
        self.assertTrue(pu.check_for_layers(packet, "ssdp"))
        capture.close()

    def test_arp(self):
        # Check number of layers in all kinds of packets
        file_path = os.path.join(test_directory, "arp.pcapng")
        capture = ps.FileCapture(file_path, only_summaries=False)
        packet = capture[0]
        self.assertTrue(pu.check_number_of_layers(packet, 2))
        self.assertTrue(pu.check_for_layers(packet, "arp"))
        capture.close()


class DissectorChecks(unittest.TestCase):
    def test_speed_dissection(self):
        file_path = os.path.join(test_directory, "valid_speed.pcapng")
        capture = ps.FileCapture(file_path, only_summaries=False)
        packet = capture[0]

        byte_field = packet.udp.payload.split(":")

        sid = pu.extract_sid(byte_field)
        iid = pu.extract_iid(byte_field)

        self.assertEqual(sid, "aa00aba4")
        self.assertEqual(iid, "55005731")

        status_type = pu.compute_status_type(sid, iid)

        self.assertEqual(status_type, "SPEED")
        self.assertEqual(pu.extract_payload(byte_field, status_type), 10)

    def test_throttle_dissection(self):
        file_path = os.path.join(test_directory, "valid_throttle.pcapng")
        capture = ps.FileCapture(file_path, only_summaries=False)
        packet = capture[0]

        byte_field = packet.udp.payload.split(":")

        sid = pu.extract_sid(byte_field)
        iid = pu.extract_iid(byte_field)

        self.assertEqual(sid, "aa00aba1")
        self.assertEqual(iid, "5500572e")

        status_type = pu.compute_status_type(sid, iid)

        self.assertEqual(status_type, "THROTTLE")
        self.assertEqual(pu.extract_payload(byte_field, status_type), 10)

    def test_speed_dissection(self):
        file_path = os.path.join(test_directory, "valid_speed.pcapng")
        capture = ps.FileCapture(file_path, only_summaries=False)
        packet = capture[0]

        byte_field = packet.udp.payload.split(":")

        sid = pu.extract_sid(byte_field)
        iid = pu.extract_iid(byte_field)

        self.assertEqual(sid, "aa00aba4")
        self.assertEqual(iid, "55005731")

        status_type = pu.compute_status_type(sid, iid)

        self.assertEqual(status_type, "SPEED")
        self.assertEqual(pu.extract_payload(byte_field, status_type), 10)

    def test_throttle_dissection(self):
        file_path = os.path.join(test_directory, "valid_throttle.pcapng")
        capture = ps.FileCapture(file_path, only_summaries=False)
        packet = capture[0]

        byte_field = packet.udp.payload.split(":")

        sid = pu.extract_sid(byte_field)
        iid = pu.extract_iid(byte_field)

        self.assertEqual(sid, "aa00aba1")
        self.assertEqual(iid, "5500572e")

        status_type = pu.compute_status_type(sid, iid)

        self.assertEqual(status_type, "THROTTLE")
        self.assertEqual(pu.extract_payload(byte_field, status_type), 486)

    def test_brake_dissection(self):
        file_path = os.path.join(test_directory, "valid_brake.pcapng")
        capture = ps.FileCapture(file_path, only_summaries=False)
        packet = capture[0]

        byte_field = packet.udp.payload.split(":")

        sid = pu.extract_sid(byte_field)
        iid = pu.extract_iid(byte_field)

        self.assertEqual(sid, "aa00abc2")
        self.assertEqual(iid, "5500574f")

        status_type = pu.compute_status_type(sid, iid)

        self.assertEqual(status_type, "BRAKE")
        self.assertEqual(pu.extract_payload(byte_field, status_type), 0)

    def test_cruise_dissection(self):
        file_path = os.path.join(test_directory, "valid_cruise.pcapng")
        capture = ps.FileCapture(file_path, only_summaries=False)
        packet = capture[0]

        byte_field = packet.udp.payload.split(":")

        sid = pu.extract_sid(byte_field)
        iid = pu.extract_iid(byte_field)

        self.assertEqual(sid, "aa00ab9b")
        self.assertEqual(iid, "55005728")

        status_type = pu.compute_status_type(sid, iid)

        self.assertEqual(status_type, "CRUISE")
        self.assertEqual(pu.extract_payload(byte_field, status_type), 0)


if __name__ == "__main__":
    unittest.main()
