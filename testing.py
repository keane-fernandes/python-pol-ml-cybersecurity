""""

This is a python script that performs assert tests and unit tests on
the methods in pol_utilities.py.

"""
import pyshark as ps
import pol_utilities as pu
import os
import unittest

cwd = os.getcwd()
test_directory = os.path.join(cwd, pu.root.get("testing"))


class PacketTests(unittest.TestCase):
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

    def test_rrcp(self):
        file_path = os.path.join(test_directory, "rrcp.pcapng")
        capture = ps.FileCapture(file_path, only_summaries=False)
        packet = capture[0]
        self.assertTrue(pu.check_for_rrcp(packet))
        capture.close()

    def test_dhcp(self):
        file_path = os.path.join(test_directory, "dhcp.pcapng")
        capture = ps.FileCapture(file_path, only_summaries=False)
        packet = capture[0]
        self.assertTrue(pu.check_number_of_layers(packet, 4))
        self.assertTrue(pu.check_for_layers(packet, "dhcp"))
        capture.close()

        file_path = os.path.join(test_directory, "dhcpv6.pcapng")
        capture = ps.FileCapture(file_path, only_summaries=False)
        packet = capture[0]
        self.assertTrue(pu.check_number_of_layers(packet, 4))
        self.assertTrue(pu.check_for_layers(packet, "dhcpv6"))
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
        file_path = os.path.join(test_directory, "arp.pcapng")
        capture = ps.FileCapture(file_path, only_summaries=False)
        packet = capture[0]
        self.assertTrue(pu.check_for_arp(packet))
        self.assertEqual(pu.retrieve_sid("arp"), "gggggggg")
        self.assertEqual(pu.retrieve_iid("arp"), "gggggggg")
        self.assertEqual(
            pu.compute_status_type(pu.retrieve_sid("arp"), pu.retrieve_iid("arp")),
            "ARP",
        )
        capture.close()

    def test_nbns(self):
        file_path = os.path.join(test_directory, "nbns.pcapng")
        capture = ps.FileCapture(file_path, only_summaries=False)
        packet = capture[0]
        self.assertTrue(pu.check_for_nbns(packet))
        self.assertEqual(pu.retrieve_sid("nbns"), "hhhhhhhh")
        self.assertEqual(pu.retrieve_iid("nbns"), "hhhhhhhh")
        self.assertEqual(
            pu.compute_status_type(pu.retrieve_sid("nbns"), pu.retrieve_iid("nbns")),
            "NBNS",
        )
        capture.close()

    def test_llmnr(self):
        file_path = os.path.join(test_directory, "llmnr.pcapng")
        capture = ps.FileCapture(file_path, only_summaries=False)
        packet = capture[0]
        self.assertTrue(pu.check_for_llmnr(packet))
        self.assertEqual(pu.retrieve_sid("llmnr"), "iiiiiiii")
        self.assertEqual(pu.retrieve_iid("llmnr"), "iiiiiiii")
        self.assertEqual(
            pu.compute_status_type(pu.retrieve_sid("llmnr"), pu.retrieve_iid("llmnr")),
            "LLMNR",
        )
        capture.close()

    def test_malformed(self):
        file_path = os.path.join(test_directory, "malformed.pcapng")
        capture = ps.FileCapture(file_path, only_summaries=False)
        packet = capture[0]
        self.assertTrue(pu.check_for_malformed(packet))
        self.assertEqual(pu.retrieve_sid("malformed"), "jjjjjjjj")
        self.assertEqual(pu.retrieve_iid("malformed"), "jjjjjjjj")
        self.assertEqual(
            pu.compute_status_type(
                pu.retrieve_sid("malformed"), pu.retrieve_iid("malformed")
            ),
            "MALFORMED",
        )
        capture.close()


class DissectorTests(unittest.TestCase):
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


class UtilityTests(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()
