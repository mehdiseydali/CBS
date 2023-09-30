The code that provided in session features.py file extracts statistical features from network traffic sessions in PCAP files and saves them to a CSV file. The features extracted are:

Interarrival times: Minimum, maximum, median, and standard deviation of the time between packets in a session.
Packet lengths: Minimum, maximum, median, and standard deviation of the packet lengths in a session.
Payload sizes: Minimum, maximum, median, and standard deviation of the payload sizes in a session.
Session duration: Total time of the session.
Active time: Total time that packets were being sent or received in the session.
Idle time: Total time that there was no packet activity in the session.
Packet truncation: Number of packets that were truncated in the session.
Total packets: Total number of packets in the session.
Bytes per second: Average number of bytes transmitted per second in the session.
Packets per second: Average number of packets transmitted per second in the session.
The code works by first reading the PCAP files and extracting the packets. Then, it groups the packets into sessions based on the source IP address, destination IP address, source port, and destination port. For each session, the code calculates the statistical features listed above. Finally, the code saves the statistical features to a CSV file.

This code can be used to extract statistical features from network traffic for a variety of purposes, such as:

Network traffic analysis: The statistical features can be used to identify patterns and trends in network traffic. This information can be used to improve network performance and security.
Network intrusion detection: The statistical features can be used to develop machine learning models to detect malicious network traffic.
Network performance monitoring: The statistical features can be used to monitor the performance of network applications and services.
Overall, the code  provided is a useful tool for extracting statistical features from network traffic sessions./
