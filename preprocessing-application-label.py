import scapy.all as scapy
import csv

def get_application_from_filename(filename):
  """Gets the application of a packet from the filename.

  Args:
    filename: The filename of the packet.

  Returns:
    The application of the packet, or None if the application cannot be determined.
  """

  # Get the prefix of the filename.
  prefix = filename.split(".")[0].lower()

  # Determine the application based on the prefix.
  if prefix == "Icq":
    application = "Icq"
  elif prefix == "Chat_facebook":
    application = "Chat_facebook"
  elif prefix == "Chat_Hangout":
    application = "Chat_Hangout"
  elif prefix == "Chat_gmail":
    application = "Chat_gmail"
  elif prefix == "Chat_Skype":
    application = "Chat_Skype"
  elif prefix == "Email":
    application = "Email"
  elif prefix == "Gmail":
    application = "Gmail"
  elif prefix == "FTPS":
    application = "FTPS"
  elif prefix == "SFTP":
    application = "SFTP"
  elif prefix == "SCP":
    application = "SCP"
  elif prefix == "FTP_SKype":
    application = "FTP_SKype"
  elif prefix == "Torrent":
    application = "Torrent"
  elif prefix == "Yuotube":
    application = "Yuotube"
  elif prefix == "Netflix":
    application = "Netflix"
  elif prefix == "Spotify":
    application = "Spotify"
  elif prefix == "Vimo":
    application = "Vimo"    
  elif prefix == "Streamig_Skype":
    application = "Streamig_Skype"
  elif prefix == "Voip_Skype":
    application = "Voip_Skype"
  elif prefix == "Voipbuster":
    application = "Voipbuster"
  elif prefix == "Voip_Hangout":
    application = "Voip_Hangout"
  elif prefix == "Voip_facebook":
    application = "Voip_facebook"    
  else:
    application = None

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

def preprocess_iscx_vpn_nonvpn_dataset(pcap_path, output_csv_path):
  """Pre-processes the ISCX VPN-NonVPN dataset and saves the application of each packet to a CSV file.

  Args:
    pcap_path: The path to the ISCX VPN-NonVPN dataset PCAP file.
    output_csv_path: The path to the CSV file to save the application of each packet to.
  """

  # Read the PCAP file.
  packets = scapy.rdpcap(pcap_path)

  # Create a CSV file to save the application of each packet to.
  with open(output_csv_path, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Application", "Label"])

    # Iterate over the packets and write the application and label of each packet to the CSV file.
    for packet in packets:
      # Get the application and label of the packet.
      application = get_application_from_filename(pcap_path.name)
      label = get_label(pcap_path.name)

      # If the application and label could be determined, write them to the CSV file.
      if application is not None and label is not None:
        writer.writerow([application, label])

if __name__ == "__main__":
  # The path to the ISCX VPN-NonVPN dataset PCAP file.
  pcap_path = "/path/to/iscx_vpn_nonvpn_dataset.pcap"

  # The path to the CSV file to save the application of each packet to.
  output_csv_path = "/path/to/output.csv"

  # Pre-process the ISCX VPN-NonVPN dataset and save the application of each packet to a CSV file.
  preprocess_iscx_vpn_nonvpn_dataset(pcap_path, output_csv_path)