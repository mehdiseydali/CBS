import os
import csv
from scapy.all import *

# Function to mask the IP layer header
def ip_mask(packet):
    if IP in packet:
        packet[IP].src = '0.0.0.0'
        packet[IP].dst = '0.0.0.0'

# Function to normalize a packet's byte values to [0-1]
def normalize_packet(packet):
    if Raw in packet:
        raw_data = bytes(packet[Raw])
        normalized_data = [byte / 255.0 for byte in raw_data]
        packet[Raw].load = bytes(normalized_data)

# Function to split and pad packets if length > 1500
def split_and_pad(packet):
    if len(packet) > 1500:
        num_packets = len(packet) // 1500 + 1
        split_packets = [packet[i:i + 1500] for i in range(0, len(packet), 1500)]
        for i in range(num_packets):
            if len(split_packets[i]) < 1500:
                split_packets[i] += b'\x00' * (1500 - len(split_packets[i]))
        return split_packets
    else:
        return [packet]

# Function to categorize file types based on the filename
def categorize_file_type(filename):
    if "vpn" in filename:
        if "chat" in filename:
            return 1
        elif "email" in filename:
            return 3
        elif any(word in filename for word in ["facebook_audio", "hangouts_audio", "skype_audio", "voip"]):
            return 5
        elif any(word in filename for word in ["ftp", "file", "scp", "sftp"]):
            return 7
        elif any(word in filename for word in ["vimeo", "youtube", "netflix", "hangouts_video", "facebook_video", "skype_video"]):
            return 9
        elif "Torrent01" in filename:
            return 11
        elif "tor" in filename:
            return 13
    else:  # Non-VPN traffic
        if "chat" in filename:
            return 0
        elif "email" in filename:
            return 2
        elif any(word in filename for word in ["facebook_audio", "hangouts_audio", "skype_audio", "voip"]):
            return 4
        elif any(word in filename for word in ["ftp", "file", "scp", "sftp"]):
            return 6
        elif any(word in filename for word in ["vimeo", "youtube", "netflix", "hangouts_video", "facebook_video", "skype_video"]):
            return 8
        elif "Torrent01" in filename:
            return 10
        elif "tor" in filename:
            return 14
    return None

# Path to the directory containing PCAP files
pcap_directory = '/path/to/pcap/files'

# Create a CSV file for saving normalized packets
csv_file = open('normalized_packets.csv', 'w', newline='')
csv_writer = csv.writer(csv_file)

# Iterate through each PCAP file in the directory
for pcap_file in os.listdir(pcap_directory):
    if pcap_file.endswith('.pcap'):
        label = categorize_file_type(pcap_file)
        if label is not None:
            packets = rdpcap(os.path.join(pcap_directory, pcap_file))

            for packet in packets:
                if Raw in packet and packet.haslayer(Ether) and packet[Ether].type == 0x800:
                    ip_mask(packet)
                    normalized_packets = split_and_pad(packet)
                    for normalized_packet in normalized_packets:
                        normalize_packet(normalized_packet)
                        csv_writer.writerow([bytes(normalized_packet), label])

# Close the CSV file
csv_file.close()
