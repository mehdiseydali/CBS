"""
The code you have provided is a function called histogram_Dataset(). This function plots a histogram of the packet lengths in a set of pcap files.

The function first defines two lists, pkt_numebr_list and pkt_length_list. The pkt_numebr_list stores the packet numbers in the pcap files. The pkt_length_list stores the lengths of the packets in the pcap files.

The function then iterates over the pcap files in the files list. For each pcap file, the function reads the packets in the file and adds the packet numbers and lengths to the pkt_numebr_list and pkt_length_list lists, respectively.

The function then calculates the probability mass function (PMF) of the packet lengths. The PMF is a function that gives the probability of a packet having a particular length.

The function then plots a histogram of the PMF. The histogram is a bar chart that shows the number of packets with each length.

The function finally returns the plot.

The first few lines define the pkt_numebr_list and pkt_length_list lists.

The next few lines iterate over the pcap files in the files list. For each pcap file, the function reads the packets in the file and adds the packet numbers and lengths to the pkt_numebr_list and pkt_length_list lists, respectively.

The next few lines calculate the PMF of the packet lengths.

The next few lines plot the histogram of the PMF.

The final line returns the plot.
"""


def histogram_Dataset(files,path):

    pkt_numebr_list = []
    pkt_length_list =[]
    n_200 = 0
    n_400 = 0
    n_600 = 0
    n_800 = 0
    n_1000 = 0
    n_1200 = 0
    n_1500 = 0
    bigger_1500 = 0
    for f in files:
        print('befor reading time is :{}'.format(datetime.now().time()))
        packets = rdpcap(os.path.join(path, f))
        print('after reading time is :{}'.format(datetime.now().time()))
        for i in range(len(packets)):
            pkt_numebr_list.append(i)
            pkt_length_list.append(len(packets[i]))
    # in this section we calculate PMF of packet lenght
    packet_lenght_data = dict((x, pkt_length_list.count(x)) for x in set(pkt_length_list))
    key_max = max(packet_lenght_data.keys(), key=(lambda k: packet_lenght_data[k]))
    key_min = min(packet_lenght_data.keys(), key=(lambda k: packet_lenght_data[k]))
    pkt_lenght = list(packet_lenght_data.keys())
    values = list(packet_lenght_data.values())
    total_packets = sum(values)
    
    # naming the x-axis
    plt.xlabel('Packet Lenght')
    # naming the y-axis
    plt.ylabel('PMF')
    # plot title
    plt.title('Packet Lenght Distribution Map')
    
    for i in range(len(pkt_lenght)):
        if(pkt_lenght[i]>=0 and pkt_lenght[i]<=200):
            n_200 = n_200 + values[i]
        elif(pkt_lenght[i]>200 and pkt_lenght[i]<=400):
            n_400 = n_400 + values[i]
        elif(pkt_lenght[i]>400 and pkt_lenght[i]<=600):
            n_600 = n_600 + values[i]
        elif(pkt_lenght[i]>600 and pkt_lenght[i]<=800):
            n_800 = n_800 + values[i]
        elif(pkt_lenght[i]>800 and pkt_lenght[i]<=1000):
            n_1000 = n_1000 + values[i]
        elif(pkt_lenght[i]>1000 and pkt_lenght[i]<=1200):
            n_1200 = n_1200 + values[i]
        elif(pkt_lenght[i]>1200 and pkt_lenght[i]<=1500):
            n_1500 = n_1500 + values[i]
        else:
            bigger_1500 = bigger_1500 + values[i]
    # setting ticks for x-axis
    x_tickes = [n_200,n_400,n_600,n_800,n_1000,n_1200,n_1500,bigger_1500]
    x_ticklabels = ['0-200', '200-400', '400-600', '600-800','800-1000'
                    ,'1000-1200','1200-1500','1500-bigger']
    y_tickes = [round((x/total_packets)) for x in x_tickes ]
    y_tickLabels = [0,15,30,45,60,75,90,100]
   
    plt.bar(x_ticklabels, y_tickes, color ='maroon',width =0.4)
    plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter(1))
    
    plt.show()

    return