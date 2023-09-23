"""
The code you have provided is a function called process_metadata_pcap(). This function reads a pcap file and prints the metadata of the first and the last packets in the connection between the two hosts specified by the client and server parameters.

The function first opens the pcap file and gets the number of packets in the file. It then iterates over the packets in the file. For each packet, the function first creates an Ether object from the packet data. The Ether class in the packet library represents an Ethernet packet. The function then checks if the type field of the Ether object is equal to 0x0800. If it is, then the packet is an IPv4 packet.

The function then checks if the proto field of the IP object is equal to 6. If it is, then the packet is a TCP packet.

The function then checks if the source or destination IP address of the packet matches the client or server parameter. If it does, then the function increments the interesting_packet_count variable.

If the packet is an interesting packet, then the function checks if it is the first or the last packet in the connection. If it is, then the function stores the timestamp and ordinal number of the packet.

Finally, the function prints the total number of packets in the file, the number of interesting packets, and the timestamps and ordinal numbers of the first and the last packets in the connection.


"""

# In this code iteration, we’ll access the packet’s metadata;
# in particular the timestamps and ordinal numbers (i.e. packet number within the packet capture) of the first and the last packets of the connection that we’re interested in.
def process_metadata_pcap(file_name):
    print('Opening {}...'.format(file_name))

    client = '192.168.43.75:54732'
    server = '172.217.22.78:443'

    (client_ip, client_port) = client.split(':')
    (server_ip, server_port) = server.split(':')

    count = 0
    interesting_packet_count = 0
    first_pkt_timestamp = 0
    first_pkt_ordinal = 0
    first_pkt_timestamp_resolution= 0
    last_pkt_ordinal = 0
    last_pkt_timestamp_resolution = 0

    for (pkt_data, pkt_metadata,) in RawPcapReader(file_name):
        count += 1
        ether_pkt = Ether(pkt_data)
        if 'type' not in ether_pkt.fields:
            # LLC frames will have 'len' instead of 'type'.
            # We disregard those
            continue

        if ether_pkt.type != 0x0800:
            # disregard non-IPv4 packets
            continue

        ip_pkt = ether_pkt[IP]

        if ip_pkt.proto != 6:
            # Ignore non-TCP packet
            continue

        if (ip_pkt.src != server_ip) and (ip_pkt.src != client_ip):
            # Uninteresting source IP address
            continue

        if (ip_pkt.dst != server_ip) and (ip_pkt.dst != client_ip):
            # Uninteresting destination IP address
            continue

        tcp_pkt = ip_pkt[TCP]

        if (tcp_pkt.sport != int(server_port)) and \
                (tcp_pkt.sport != int(client_port)):
            # Uninteresting source TCP port
            continue

        if (tcp_pkt.dport != int(server_port)) and \
                (tcp_pkt.dport != int(client_port)):
            # Uninteresting destination TCP port
            continue

        interesting_packet_count += 1
        if interesting_packet_count == 1:
            first_pkt_timestamp = (pkt_metadata.tshigh << 32) | pkt_metadata.tslow
            first_pkt_timestamp_resolution = pkt_metadata.tsresol
            first_pkt_ordinal = count

        last_pkt_timestamp = (pkt_metadata.tshigh << 32) | pkt_metadata.tslow
        last_pkt_timestamp_resolution = pkt_metadata.tsresol
        last_pkt_ordinal = count
    # ---

    print('{} contains {} packets ({} interesting)'.
          format(file_name, count, interesting_packet_count))

    print('First packet in connection: Packet #{} {}'.
          format(first_pkt_ordinal,
                 printable_timestamp(first_pkt_timestamp,
                                     first_pkt_timestamp_resolution)))
    print(' Last packet in connection: Packet #{} {}'.
          format(last_pkt_ordinal,
                 printable_timestamp(last_pkt_timestamp,
                                     last_pkt_timestamp_resolution)))
def printable_timestamp(ts, resol):
    ts_sec = ts // resol
    ts_subsec = ts % resol
    ts_sec_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ts_sec))
    return '{}.{}'.format(ts_sec_str, ts_subsec)