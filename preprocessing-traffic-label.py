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
# Create a dictionary to map prefixes to application names
    prefix_to_application = {
        'icq': 'Icq',
	'aim-chat': 'AIM-Chat'
        'chat_facebook': 'chat_facebook',
        'chat_hangout': 'chat_hangout',
        'chat_gmail': 'chat_gmail',
        'chat_skype': 'chat_skype',
        'email': 'email',
        'gmail': 'gmail',
        'ftps': 'ftps',
        'sftp': 'sftp',
        'scp': 'scp',
        'ftp_skype': 'ftp_skype',
        'torrent': 'torrent',
	'tor': 'tor', 
        'youtube': 'youtube',
        'netflix': 'netflix',
        'spotify': 'spotify',
        'vimeo': 'vimeo',
        'streaming_skype': 'streaming_skype',
        'voip_skype': 'voip_skype',
        'voipbuster': 'Voipbuster',
        'voip_hangout': 'voipbuster',
        'voip_facebook': 'voip_facebook'
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
def read_app_pcap_files():
    #file_list = [x for x in os.listdir('/home/mehdi') if x.endswith(".pcap")]
    #print(file_list)
    root_dir = '/media/mehdi/linux/data/CompletePCAPs'
    file_name_list_full_path = []
    file_name_list = []
    file_name_dict = {}
    for path in os.listdir(root_dir):
        full_path = os.path.join(root_dir, path)
        if os.path.isfile(full_path) and (path.endswith(".pcap") or path.endswith("pcapng")):
            print(full_path)
            file_name_list_full_path.append(full_path)
            file_name_list.append(path)

    # find category of ISCX VPN-NONVPN DATASET
    for i in range(len(file_name_list_full_path)):
	    app_name = get_application_from_filename(file_name_list_full_path[i])
	if "icq" in app_name:
            file_name_dict[file_name_list_full_path[i]] = 1 #"vpn icq"
        elif "chat_facebook" in app_name:
            file_name_dict[file_name_list_full_path[i]] = 2 #"chat_facebook"
        elif "chat_hangout" in app_name:
            file_name_dict[file_name_list_full_path[i]] = 3 #"chat_hangout"
        elif "chat_gmail" in app_name:
            file_name_dict[file_name_list_full_path[i]] = 4 #"chat_gmail"
        elif "chat_skype" in app_name:
            file_name_dict[file_name_list_full_path[i]] = 5 #"chat_skype"
        elif "email" in app_name:
            file_name_dict[file_name_list_full_path[i]] = 6 #"email"
        elif "gmail" in app_name:
            file_name_dict[file_name_list_full_path[i]] = 4 #"gmail"
	elif "ftps" in app_name:
            file_name_dict[file_name_list_full_path[i]] = 7 #"ftps"
	elif "sftp" in app_name:
            file_name_dict[file_name_list_full_path[i]] = 8 #"sftp"
	elif "scp" in app_name:
            file_name_dict[file_name_list_full_path[i]] = 9 #"scp"
	elif "ftp_skype" in app_name:
            file_name_dict[file_name_list_full_path[i]] = 5 #"ftp_skype"
	elif "torrent" in app_name:
            file_name_dict[file_name_list_full_path[i]] = 10 #"torrent"
	elif "youtube" in app_name:
            file_name_dict[file_name_list_full_path[i]] = 11 #"youtube"
	elif "netflix" in app_name:
            file_name_dict[file_name_list_full_path[i]] = 12 #"netflix"
	elif "spotify" in app_name:
            file_name_dict[file_name_list_full_path[i]] = 13 #"spotify"
	elif "vimeo" in app_name:
            file_name_dict[file_name_list_full_path[i]] = 14 #"vimeo"
        elif "streaming_skype" in app_name:
            file_name_dict[file_name_list_full_path[i]] = 5 #"streaming_skype"
        elif "voip_skype" in app_name:
            file_name_dict[file_name_list_full_path[i]] = 5 #"voip_skype"
        elif "voipbuster" in app_name:
            file_name_dict[file_name_list_full_path[i]] = 15 #"voipbuster"			
	elif "voip_hangout" in app_name:
            file_name_dict[file_name_list_full_path[i]] = 3 #"voip_hangout"
	elif "voip_facebook" in app_name:
            file_name_dict[file_name_list_full_path[i]] = 2 #"voip_facebook"		
	elif "aim-chat" in app_name:
            file_name_dict[file_name_list_full_path[i]] = 16 #"AIM-Chat"
	elif "tor" in app_name:
            file_name_dict[file_name_list_full_path[i]] = 17 #"tor"	
	else:
                pass 
            
        
    print(file_name_dict)
    exctracted_root_dir = load_pcap_datatype(file_name_dict)

    return exctracted_root_dir
def read_app_pacap_load()
	# Path to the directory containing PCAP files
	pcap_directory = '/path/to/pcap/files'

	# Create a CSV file for saving normalized packets
	csv_file = open('normalized_packets.csv', 'w', newline='')
	csv_writer = csv.writer(csv_file)

	# Iterate through each PCAP file in the directory
	or pcap_file in os.listdir(pcap_directory):
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
