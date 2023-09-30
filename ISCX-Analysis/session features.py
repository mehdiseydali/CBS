import os
import pandas as pd
from scapy.all import rdpcap
from collections import defaultdict
import statistics

# Function to calculate statistical features
def calculate_statistics(values):
    if not values:
        return None, None, None, None  # Return None for min, max, median, and standard deviation if the list is empty
    return min(values), max(values), statistics.median(values), statistics.stdev(values)

# Initialize data structures
session_data = defaultdict(list)

# Replace 'path/to/your/dataset/folder' with the actual path to your dataset folder
dataset_folder = 'path/to/your/dataset/folder'
output_csv = 'session_stats.csv'

# List of PCAP files in the dataset folder
pcap_files = [file for file in os.listdir(dataset_folder) if file.endswith('.pcap')]

# Loop through the PCAP files
for pcap_file in pcap_files:
    pcap_path = os.path.join(dataset_folder, pcap_file)
    packets = rdpcap(pcap_path)
    current_session = []
    last_time = None

    # Loop through the packets in the PCAP file
    for packet in packets:
        if 'IP' in packet and 'TCP' in packet:
            session_key = (packet['IP'].src, packet['IP'].dst, packet['TCP'].sport, packet['TCP'].dport)
            if not current_session:
                current_session.append(packet)
            else:
                inter_arrival_time = packet.time - last_time
                current_session.append(packet)
                if packet['TCP'].flags & 0x02:  # Check if it's a SYN packet (start of a new session)
                    if session_key not in session_data:
                        session_data[session_key] = {
                            'InterarrivalTimes': [],
                            'PacketLengths': [],
                            'PayloadSizes': [],
                            'SessionDuration': 0
                        }
                    session_data[session_key]['InterarrivalTimes'].append(inter_arrival_time)
                    session_data[session_key]['PacketLengths'].append(len(packet))
                    if 'Raw' in packet:
                        session_data[session_key]['PayloadSizes'].append(len(packet['Raw']))
                    current_session = []
            last_time = packet.time

# Initialize lists to store the calculated features
session_features = []

# Loop through the sessions and calculate the features
for session_key, session_info in session_data.items():
    interarrival_min, interarrival_max, interarrival_median, interarrival_std = calculate_statistics(session_info['InterarrivalTimes'])
    packet_length_min, packet_length_max, packet_length_median, packet_length_std = calculate_statistics(session_info['PacketLengths'])
    payload_size_min, payload_size_max, payload_size_median, payload_size_std = calculate_statistics(session_info['PayloadSizes'])
    session_duration = sum(session_info['InterarrivalTimes'])
    active_time_min, active_time_max, active_time_median, active_time_std = calculate_statistics([session_duration])
    idle_time_min, idle_time_max, idle_time_median, idle_time_std = calculate_statistics([session_duration - sum(session_info['InterarrivalTimes'])])
    total_packets = len(session_info['InterarrivalTimes']) + 1  # Adding 1 to account for the first packet
    packet_truncation = total_packets - len(session_info['InterarrivalTimes']) - 1  # Subtracting 1 to account for the last packet

    bytes_per_second = sum(session_info['PacketLengths']) / session_duration
    packets_per_second = total_packets / session_duration

    session_features.append({
        'Session': session_key,
        'Min_Interarrival': interarrival_min,
        'Max_Interarrival': interarrival_max,
        'Median_Interarrival': interarrival_median,
        'Std_Interarrival': interarrival_std,
        'Min_Packet_Length': packet_length_min,
        'Max_Packet_Length': packet_length_max,
        'Median_Packet_Length': packet_length_median,
        'Std_Packet_Length': packet_length_std,
        'Min_Payload_Size': payload_size_min,
        'Max_Payload_Size': payload_size_max,
        'Median_Payload_Size': payload_size_median,
        'Std_Payload_Size': payload_size_std,
        'Min_Active_Time': active_time_min,
        'Max_Active_Time': active_time_max,
        'Median_Active_Time': active_time_median,
        'Std_Active_Time': active_time_std,
        'Min_Idle_Time': idle_time_min,
        'Max_Idle_Time': idle_time_max,
        'Median_Idle_Time': idle_time_median,
        'Std_Idle_Time': idle_time_std,
        'Packet_Truncation': packet_truncation,
        'Total_Packets': total_packets,
        'Session_Duration': session_duration,
        'Bytes_Per_Second': bytes_per_second,
        'Packets_Per_Second': packets_per_second
    })

# Create a DataFrame from the session features
df = pd.DataFrame(session_features)

# Save the statistical features to a CSV file
df.to_csv(output_csv, index=False)
