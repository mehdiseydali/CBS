import os
import csv
from scapy.all import *
def get_application_from_filename(filename):
  """Gets the application of a packet from the filename.

  Args:
    filename: The filename of the packet.

  Returns:
    The application of the packet, or None if the application cannot be determined.
  """
"""
  # Get the prefix of the filename.
  prefix = filename.split(".")[0].lower()

  # Determine the application based on the prefix.
  # Determine the application based on the prefix.
  if re.search(r'\bicq\b', prefix):
    application = "Icq"
  elif re.search(r'\bchat_facebook\b', prefix):
    application = "Chat_facebook"
  elif re.search(r'\bchat_hangout\b', prefix):
    application = "Chat_Hangout"
  elif re.search(r'\bchat_gmail\b', prefix):
    application = "Chat_gmail"
  elif re.search(r'\bchat_skype\b', prefix):
    application = "Chat_Skype"
  elif re.search(r'\bemail\b', prefix):
    application = "Email"
  elif re.search(r'\bgmail\b', prefix):
    application = "Gmail"
  elif re.search(r'\bftps\b', prefix):
    application = "FTPS"
  elif re.search(r'\bsftp\b', prefix):
    application = "SFTP"
  elif re.search(r'\bscp\b', prefix):
    application = "SCP"
  elif re.search(r'\bftp_skype\b', prefix):
    application = "FTP_SKype"
  elif re.search(r'\btorrent\b', prefix):
    application = "Torrent"
  elif re.search(r'\byoutube\b', prefix):
    application = "Yuotube"
  elif re.search(r'\bnetflix\b', prefix):
    application = "Netflix"
  elif re.search(r'\bspotify\b', prefix):
    application = "Spotify"
  elif re.search(r'\bvimo\b', prefix):
    application = "Vimo"    
  elif re.search(r'\bstreaming_skype\b', prefix):
    application = "Streamig_Skype"
  elif re.search(r'\bvoip_skype\b', prefix):
    application = "Voip_Skype"
  elif re.search(r'\bvoipbuster\b', prefix):
    application = "Voipbuster"
  elif re.search(r'\bvoip_hangout\b', prefix):
    application = "Voip_Hangout"
  elif re.search(r'\bvoip_facebook\b', prefix):
    application = "Voip_facebook"    
  else:
    application = None

  return application
  """
# Create a dictionary to map prefixes to application names
    prefix_to_application = {
        'icq': 'Icq',
        'chat_facebook': 'Chat_facebook',
        'chat_hangout': 'Chat_Hangout',
        'chat_gmail': 'Chat_gmail',
        'chat_skype': 'Chat_Skype',
        'email': 'Email',
        'gmail': 'Gmail',
        'ftps': 'FTPS',
        'sftp': 'SFTP',
        'scp': 'SCP',
        'ftp_skype': 'FTP_Skype',
        'torrent': 'Torrent',
        'youtube': 'Yuotube',
        'netflix': 'Netflix',
        'spotify': 'Spotify',
        'vimo': 'Vimo',
        'streaming_skype': 'Streamig_Skype',
        'voip_skype': 'Voip_Skype',
        'voipbuster': 'Voipbuster',
        'voip_hangout': 'Voip_Hangout',
        'voip_facebook': 'Voip_facebook'
    }

    # Get the prefix of the filename and convert it to lowercase
    prefix = filename.split(".")[0].lower()

    # Use the dictionary to determine the application
    application = prefix_to_application.get(prefix, None)

    return application

def get_label(filename):
  """Gets the label of a packet from the filename.

  Args:
    filename: The filename of the packet.

  Returns:
    The label of the packet, or None if the label cannot be determined.
  """

  # Get the prefix of the filename.
  prefix = filename.split(".")[0].lower()

  # Determine the label based on the prefix.
  if prefix.startswith("vpn_"):
    label = "VPN"
  else:
    label = "Non-VPN"

  return label
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
        application = get_application_from_filename(pcap_path.name)
        app_label = get_label(pcap_path.name)
        if label is not None:
            packets = rdpcap(os.path.join(pcap_directory, pcap_file))

            for packet in packets:
                if Raw in packet and packet.haslayer(Ether) and packet[Ether].type == 0x800:
                    ip_mask(packet)
                    normalized_packets = split_and_pad(packet)
                    for normalized_packet in normalized_packets:
                        normalize_packet(normalized_packet)
                        csv_writer.writerow([bytes(normalized_packet), label,application+app_label])

# Close the CSV file
csv_file.close()
