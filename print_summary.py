"""
The code you have provided is a function called print_summary(). This function takes a packet as input and prints the source and destination IP addresses and the source and destination TCP ports of the packet.

The function first checks if the packet contains an IP layer. If it does, then the function gets the source and destination IP addresses of the packet.

The function then checks if the packet contains a TCP layer. If it does, then the function gets the source and destination TCP ports of the packet.

Finally, the function prints the source and destination IP addresses and the source and destination TCP ports of the packet.

The first line checks if the packet contains an IP layer. The IP layer is a required layer for all IP packets. If the packet does not contain an IP layer, then the function does not print anything.

The second line gets the source IP address of the packet. The src attribute of the IP object returns the source IP address of the packet.

The third line gets the destination IP address of the packet. The dst attribute of the IP object returns the destination IP address of the packet.

The fourth line checks if the packet contains a TCP layer. The TCP layer is not a required layer for all IP packets. If the packet does not contain a TCP layer, then the function does not print anything.

The fifth line gets the source TCP port of the packet. The sport attribute of the TCP object returns the source TCP port of the packet.

The sixth line gets the destination TCP port of the packet. The dport attribute of the TCP object returns the destination TCP port of the packet.

Finally, the seventh and eighth lines print the source and destination IP addresses and the source and destination TCP ports of the packet.

"""
def print_summary(pkt):
    if IP in pkt:
        ip_src=pkt[IP].src
        ip_dst=pkt[IP].dst
        print(' IP src is: {}'.format(str(ip_src)))
        print(' IP dst is: {}'.format(str(ip_dst)))
    if TCP in pkt:
        tcp_sport=pkt[TCP].sport
        tcp_dport=pkt[TCP].dport
        print(' TCP sport is: {}'.format(str(tcp_sport)))
        print(' TCP dport is: {}'.format(str(tcp_dport)))