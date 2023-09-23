"""
The code you have provided is a function called extract_header_payload_packets(). This function extracts the header and payload information from packets in a pcap file and saves it to a CSV file.

The function first defines a few variables, such as the default MTU, the number of packets to flush to the CSV file at a time, and a flag to indicate whether the CSV file has been created yet.

The function then iterates over the packets in the pcap file. For each packet, the function checks if the packet has a payload. If the packet does have a payload, the function extracts the header and payload information from the packet and saves it to a DataFrame.

If the packet is larger than the MTU, the function breaks the packet up into multiple packets and saves each of the smaller packets to the DataFrame.

Once the function has processed all of the packets in the pcap file, it flushes the DataFrame to the CSV file.
"""
from ip_masking import ip_masking

def extract_header_payload_packets(packets,k,v):
    print('file name processing: {}'.format(k))
    default_mtu = 1500
    # flush counter for flusshing packet to csv file
    number_of_pck = len(packets)
    flush_counter = 10000
    if(number_of_pck <= flush_counter):
        flush_counter = number_of_pck
    has_flushed = False
    # counter for checking how many valid packet has been processed
    total_processed_packet = 0
    temp_processed_packet = 0
    # root address for saving extracket packet data is set here
    extracted_packet_root_dir =  '/media/mehdi/linux/data/must_be_normalized_data/'
    processed_file_name =b''
    # create extracted data packet folder as name  extracted_packet_root_dir
    if not os.path.exists(extracted_packet_root_dir):
        os.makedirs(extracted_packet_root_dir)
    # Find All Protocol supported by Scapy
    f = io.StringIO()
    protocol = [] # list of all Protocol
    with redirect_stdout(f):
        ls()
    out = f.getvalue()
    #print("Packet Listing:", out, sep="\n\n")
    protocol_list = out.split('\n')
    for i in range(len(protocol_list)):
        protocol.append(protocol_list[i].split(':')[0].replace(" ", ""))
    # Create DataFrame for packet
    df = pd.DataFrame(columns=['Source_IP', 'Dest_IP', 'Source_Port', 'Destination_Port','pckt_protocol',
                               'src_MAC', 'dst_MAC', 'pckt_ttl','payload','ip_header','packet_lenght','packet_data_lenght','packet_number','class_label'])
    
    pkt_count = 0
    # List to holds srpIPs
    srpIP = []
    tls_ip = [field.name for field in TLS().fields_desc]
    print(tls_ip)
    cnt = 0
    pkt_number = 0
    pktlst = []
    # Read each packet and appent to srpIP list
    for pkt in packets:
        pkt_number += 1
        
        if(pkt_number == 40):
            print("893")

        print("packet number  :{} has been proccessed".format(pkt_number))
        has_payload = False
        if(pkt.haslayer(Raw)):
            try:
                if (pkt.haslayer(SSLv2)):
                    print("sslv2 layer")

                pck_load = TLS(pkt.load)
                if pck_load.haslayer('TLS'):
                    #records = pkt['TLS'].records
                    print("tls layer")
                #pck_load.show()
                pck_fields = [field.name for field in pck_load.fields_desc]
                has_payload = True

            except:
                print("Oops!", sys.exc_info()[0], "occurred.")


           

        if (pkt.haslayer(TLS) == False  and has_payload == True and pck_fields.count('type') > 0 and len(pkt) >= 60):
            if (len(pck_load.fields.get("msg")) > 0 ):
                if(pck_load.msg[0].name == 'TLS Application Data'):
                    if pkt.haslayer(Ether) and pkt.haslayer(IP) and pkt.haslayer(TCP) and pkt.haslayer(Raw):
                       if pck_load.type == 23:
                            # pktlst.append(cnt-1)
                            src_mac = pkt[Ether].src
                            dst_mac = pkt[Ether].dst
                            pckt_ip_dest = pkt[IP].dst
                            pckt_ip_source = pkt[IP].src
                            pckt_ttl = pkt[IP].ttl
                            pckt_protocol = 'TLS'
                            pckt_dest_port = pkt[TCP].dport
                            pckt_src_port = pkt[TCP].sport
                            payload = binascii.hexlify(bytes(pck_load.msg[0].data))
                            payload_lenght = int(len(payload) / 2)
                            packet_lenght = len(pkt)
                            # zero padding do here
                            #if (pkt[IP].len) < 1500:
                            if (len(pkt[IP])) < 1500:
                                # find tcp header
                                p = binascii.hexlify(bytes(pkt[IP].payload)[12:13])
                                # convert hex to binary
                                binary_length = "{0:08b}".format(int(p, 16))
                                # convert binary to decimal and normalize number
                                decimal_lenght = int(binary_length, 2)
                                numbe_of_tcp_header_byte = int(decimal_lenght / 4)
                                pad_len = (1500 - len(pkt[IP])) +  5
                                pad = Padding()
                                pad.load = '\x00' * int(pad_len)
                                pkt = pkt / pad
                                tcp_header = binascii.hexlify(bytes(pkt[IP].payload)[:numbe_of_tcp_header_byte])
                                pad_payload = binascii.hexlify(bytes(pkt[Raw].payload))
                                tcp_header += payload
                                tcp_header += pad_payload
                                payload = tcp_header
                                ip_header = ip_masking(pkt)
                                df.loc[len(df.index)] = [pckt_ip_source, pckt_ip_dest, pckt_src_port, pckt_dest_port,
                                                         pckt_protocol, src_mac, dst_mac, pckt_ttl, payload, ip_header,
                                                         packet_lenght, payload_lenght, pkt_number, v]
                                # in this section flush dataframe data to csv file
                                total_processed_packet += 1
                                temp_processed_packet += 1
                                # check if csv file has been created or not
                                if (total_processed_packet == flush_counter):
                                    processed_file_name = extracted_packet_root_dir + os.path.basename(k) + '.' + 'csv'
                                    df.to_csv(processed_file_name,index = False)
                                    # empty df dataframe
                                    # Delete the first flush_counter rows
                                    temp_processed_packet = 0
                                    has_flushed = True
                                    df = df.drop(df.index[range(flush_counter)])
                                # csv file exist and must flush processed packet to it
                                else:
                                    if (temp_processed_packet == flush_counter):
                                        # Write the new data to the CSV file in append mode
                                        df.to_csv(processed_file_name, mode='a', header=False, index=False)
                                        temp_processed_packet = 0
                                        # empty df dataframe
                                        # Delete the first flush_counter rows
                                        df = df.drop(df.index[range(flush_counter)])

                            # if lenght of packet is greater that MTU w must break it up to multiple packet
                            else:
                                number_of_fragmnet_pkt = 0
                                has_reminder = False
                                # find number of byte in tcp header and find mtu
                                # find tcp header
                                p = binascii.hexlify(bytes(pkt[IP].payload)[12:13])
                                # convert hex to binary
                                binary_length = "{0:08b}".format(int(p, 16))
                                # convert binary to decimal and normalize number
                                decimal_lenght = int(binary_length, 2)
                                numbe_of_tcp_header_byte = int(decimal_lenght / 4)
                                mtu = default_mtu - 20 - (numbe_of_tcp_header_byte)
                                if(int(payload_lenght % mtu) == 0):
                                    number_of_fragmnet_pkt = int(payload_lenght / mtu)
                                else:
                                    number_of_fragmnet_pkt = int(payload_lenght/mtu) + 1
                                    has_reminder = True
                               
                                offset = 0
                                payload = b''
                                for index in range(number_of_fragmnet_pkt):
                                    if(has_reminder == False):
                                        payload += binascii.hexlify(bytes(pck_load.msg[0].data[offset: (index + 1) * mtu]))
                                        offset += mtu
                                    else:
                                        if(index == number_of_fragmnet_pkt - 1):
                                            payload += binascii.hexlify(bytes(pck_load.msg[0].data[offset: offset + int(payload_lenght % mtu)]))
                                        else:
                                            payload += binascii.hexlify(bytes(pck_load.msg[0].data[offset: (index + 1) * mtu]))
                                            offset += mtu

                                    
                                    pad_len = (1500 - ((int(len(payload) / 2)) + 20 + numbe_of_tcp_header_byte))
                                    pad = Padding()
                                    pad.load = '\x00' * int(pad_len)
                                    pkt = pkt / pad
                                    tcp_header = binascii.hexlify(bytes(pkt[IP].payload)[:numbe_of_tcp_header_byte])
                                    pad_payload = binascii.hexlify(bytes(pkt[Raw].payload))
                                    tcp_header += payload
                                    tcp_header += pad_payload
                                    payload = tcp_header
                                    ip_header = ip_masking(pkt)
                                    df.loc[len(df.index)] = [pckt_ip_source, pckt_ip_dest, pckt_src_port,
                                                             pckt_dest_port, pckt_protocol, src_mac, dst_mac, pckt_ttl, payload,
                                                             ip_header, packet_lenght, payload_lenght, pkt_number, v]
                                    payload = b''

                                    # in this section flush dataframe data to csv file
                                    total_processed_packet += 1
                                    temp_processed_packet += 1
                                    # check if csv file has been created or not
                                    if (total_processed_packet == flush_counter):
                                        processed_file_name = extracted_packet_root_dir + os.path.basename(
                                            k) + '.' + 'csv'
                                        df.to_csv(processed_file_name,index = False)
                                        # empty df dataframe
                                        # Delete the first flush_counter rows
                                        temp_processed_packet = 0
                                        has_flushed = True
                                        df = df.drop(df.index[range(flush_counter)])
                                    # csv file exist and must flush processed packet to it
                                    else:
                                        if (temp_processed_packet == flush_counter):
                                            # Write the new data to the CSV file in append mode
                                            df.to_csv(processed_file_name, mode='a', header=False, index=False)
                                            temp_processed_packet = 0
                                            # empty df dataframe
                                            # Delete the first flush_counter rows
                                            df = df.drop(df.index[range(flush_counter)])


                           


        else:
            SSL2v_flag = False
            #checke if packet is server hello message
            if (pkt.haslayer(TLS) == False and has_payload == True and pck_fields.count('type') == 0 and pck_fields.count('msg')>0 ):
                if (len(pck_load.fields.get("msg")) > 0):
                    if (pck_load.msg[0].name == 'Raw' and pck_load.name == 'SSLv2'):
                        SSL2v_flag = True
            # find source and destination mac address of packet
            if (pkt.haslayer(Ether) and pkt.haslayer(IP) and pkt.haslayer(TCP) and SSL2v_flag == False and len(pkt) >= 60) :
                res_list = [i for i, value in enumerate(protocol) if (pkt.haslayer(value) == True and value != 'TCP' and
                                                                      value != 'IP' and value != 'Ether' and value != 'Raw' and value != 'TLS')]
                # check if a tls or ssl packet
                cnt += 1
                if pkt.haslayer(TLS):
                    #print('a')
                    extra_tls_layers = pkt[TLS]
                    if pkt[TLS].type == 23:
                        payload = b''
                        app_data_layer_count = 0
                        has_tls_payload = True
                        pktlst.append(cnt - 1)
                        src_mac = pkt[Ether].src
                        dst_mac = pkt[Ether].dst
                        pckt_ip_dest = pkt[IP].dst
                        pckt_ip_source = pkt[IP].src
                        pckt_ttl = pkt[IP].ttl
                        pckt_protocol = 'TLS'
                        pckt_dest_port = pkt[TCP].dport
                        pckt_src_port = pkt[TCP].sport
                        # fetch all Application Record Layer
                        while(has_tls_payload == True):
                            payload += binascii.hexlify(bytes(extra_tls_layers.msg[0].data))
                            app_data_layer_count += 1
                            if(len(extra_tls_layers.payload) > 0):
                                extra_tls_layers = extra_tls_layers.payload
                            else:
                                has_tls_payload = False

                        #payload = binascii.hexlify(bytes(pkt[TLS])[5:int(pkt[TLS].len) + 5])
                        payload_lenght = int(len(payload) / 2)
                        packet_lenght = len(pkt)
                        # zero padding do here
                        #if (pkt[IP].len) < 1500:
                        if (len(pkt[IP])) < 1500:
                            # find tcp header
                            p = binascii.hexlify(bytes(pkt[IP].payload)[12:13])
                            # convert hex to binary
                            binary_length = "{0:08b}".format(int(p, 16))
                            # convert binary to decimal and normalize number
                            decimal_lenght = int(binary_length, 2)
                            numbe_of_tcp_header_byte = int(decimal_lenght / 4)
                            pad_len = (1500 - len(pkt[IP])) + app_data_layer_count * 5
                            pad = Padding()
                            pad.load = '\x00' * int(pad_len)
                            pkt = pkt / pad
                            tcp_header = binascii.hexlify(bytes(pkt[IP].payload)[:numbe_of_tcp_header_byte])
                            #pad_payload = binascii.hexlify(bytes(pkt[TLS].payload))
                            pad_payload = binascii.hexlify(bytes(pad.load))
                            tcp_header += payload
                            tcp_header += pad_payload
                            payload = tcp_header
                            ip_header = ip_masking(pkt)
                            df.loc[len(df.index)] = [pckt_ip_dest, pckt_ip_source, pckt_src_port, pckt_dest_port,
                                                 pckt_protocol, src_mac, dst_mac, pckt_ttl, payload, ip_header,packet_lenght,payload_lenght,pkt_number, v]
                            # in this section flush dataframe data to csv file
                            total_processed_packet += 1
                            temp_processed_packet += 1
                            # check if csv file has been created or not
                            if(total_processed_packet == flush_counter):
                                processed_file_name =  extracted_packet_root_dir + os.path.basename(k) + '.' + 'csv'
                                df.to_csv(processed_file_name,index = False)
                                # empty df dataframe
                                # Delete the first flush_counter rows
                                temp_processed_packet = 0
                                has_flushed = True
                                df = df.drop(df.index[range(flush_counter)])
                            # csv file exist and must flush processed packet to it
                            else:
                                if(temp_processed_packet == flush_counter):
                                    # Write the new data to the CSV file in append mode
                                    df.to_csv(processed_file_name, mode='a', header=False, index=False)
                                    temp_processed_packet = 0
                                    # empty df dataframe
                                    # Delete the first flush_counter rows
                                    df = df.drop(df.index[range(flush_counter)])



                        # if lenght of packet is greater that MTU w must break it up to multiple packet
                        else:
                            number_of_fragmnet_pkt = 0
                            has_reminder = False
                            # find number of byte in tcp header and find mtu
                            # find tcp header
                            p = binascii.hexlify(bytes(pkt[IP].payload)[12:13])
                            # convert hex to binary
                            binary_length = "{0:08b}".format(int(p, 16))
                            # convert binary to decimal and normalize number
                            decimal_lenght = int(binary_length, 2)
                            numbe_of_tcp_header_byte = int(decimal_lenght / 4)
                            mtu = default_mtu - 20 - (numbe_of_tcp_header_byte)
                            if (int(payload_lenght % mtu) == 0):
                                number_of_fragmnet_pkt = int(payload_lenght / mtu)
                            else:
                                number_of_fragmnet_pkt = int(payload_lenght / mtu) + 1
                                has_reminder = True
                            
                            offset = 0
                            new_payload = b''
                            for index in range(number_of_fragmnet_pkt):
                                if (has_reminder == False):
                                    new_payload += payload[offset: (index + 1) * mtu]
                                    offset += mtu
                                else:
                                    if (index == number_of_fragmnet_pkt - 1):
                                        new_payload += payload[offset: offset + int(payload_lenght % mtu)]
                                    else:
                                        new_payload += payload[offset: (index + 1) * mtu]
                                        offset += mtu
                                
                                pad_len = (1500 - (int(len(new_payload) / 2) + 20 + numbe_of_tcp_header_byte))
                                pad = Padding()
                                pad.load = '\x00' * int(pad_len)
                                pkt = pkt / pad
                                tcp_header = binascii.hexlify(bytes(pkt[IP].payload)[:numbe_of_tcp_header_byte])
                                #pad_payload = binascii.hexlify(bytes(pkt[Raw].payload))
                                pad_payload = binascii.hexlify(bytes(pad.load))
                                tcp_header += new_payload
                                tcp_header += pad_payload
                                new_payload = tcp_header
                                ip_header = ip_masking(pkt)
                                df.loc[len(df.index)] = [pckt_ip_source, pckt_ip_dest, pckt_src_port,
                                                             pckt_dest_port, pckt_protocol, src_mac, dst_mac, pckt_ttl,
                                                             new_payload,ip_header, packet_lenght, payload_lenght, pkt_number, v]
                                new_payload = b''

                                # in this section flush dataframe data to csv file
                                total_processed_packet += 1
                                temp_processed_packet += 1
                                # check if csv file has been created or not
                                if (total_processed_packet == flush_counter):
                                    processed_file_name = extracted_packet_root_dir + os.path.basename(k) + '.' + 'csv'
                                    df.to_csv(processed_file_name,index = False)
                                    # empty df dataframe
                                    # Delete the first flush_counter rows
                                    temp_processed_packet = 0
                                    has_flushed = True
                                    df = df.drop(df.index[range(flush_counter)])
                                # csv file exist and must flush processed packet to it
                                else:
                                    if (temp_processed_packet == flush_counter):
                                        # Write the new data to the CSV file in append mode
                                        df.to_csv(processed_file_name, mode='a', header=False, index=False)
                                        temp_processed_packet = 0
                                        # empty df dataframe
                                        # Delete the first flush_counter rows
                                        df = df.drop(df.index[range(flush_counter)])

                else:
                    # check if packet has pkt.load and TLS layer. some of packet has Raw data and load data
                    # and load data contain TLS data. so we must check these packet
                    if (has_payload == True ):
                        tls_payload = TLS(pkt.load)
                        if(tls_payload.name == 'TLS'):
                            if pkt[TLS].type == 23:
                                payload = b''
                                app_data_layer_count = 0
                                has_tls_payload = True
                                pktlst.append(cnt - 1)
                                src_mac = pkt[Ether].src
                                dst_mac = pkt[Ether].dst
                                pckt_ip_dest = pkt[IP].dst
                                pckt_ip_source = pkt[IP].src
                                pckt_ttl = pkt[IP].ttl
                                pckt_protocol = 'TLS'
                                pckt_dest_port = pkt[TCP].dport
                                pckt_src_port = pkt[TCP].sport
                                # fetch all Application Record Layer
                                while (has_tls_payload == True):
                                    payload += binascii.hexlify(bytes(tls_payload.msg[0].data))
                                    app_data_layer_count += 1
                                    if (len(tls_payload.payload) > 0):
                                        tls_payload = tls_payload.payload
                                    else:
                                        has_tls_payload = False

                                # payload = binascii.hexlify(bytes(pkt[TLS])[5:int(pkt[TLS].len) + 5])
                                payload_lenght = int(len(payload) / 2)
                                packet_lenght = len(pkt)
                                # zero padding do here
                                # if (pkt[IP].len) < 1500:
                                if (len(pkt[IP])) < 1500:
                                    # find tcp header
                                    p = binascii.hexlify(bytes(pkt[IP].payload)[12:13])
                                    # convert hex to binary
                                    binary_length = "{0:08b}".format(int(p, 16))
                                    # convert binary to decimal and normalize number
                                    decimal_lenght = int(binary_length, 2)
                                    numbe_of_tcp_header_byte = int(decimal_lenght / 4)
                                    pad_len = (1500 - len(pkt[IP])) + app_data_layer_count * 5
                                    pad = Padding()
                                    pad.load = '\x00' * int(pad_len)
                                    pkt = pkt / pad
                                    tcp_header = binascii.hexlify(bytes(pkt[IP].payload)[:numbe_of_tcp_header_byte])
                                    # pad_payload = binascii.hexlify(bytes(pkt[TLS].payload))
                                    pad_payload = binascii.hexlify(bytes(pad.load))
                                    tcp_header += payload
                                    tcp_header += pad_payload
                                    payload = tcp_header
                                    ip_header = ip_masking(pkt)
                                    df.loc[len(df.index)] = [pckt_ip_dest, pckt_ip_source, pckt_src_port,
                                                             pckt_dest_port,
                                                             pckt_protocol, src_mac, dst_mac, pckt_ttl, payload,
                                                             ip_header, packet_lenght, payload_lenght, pkt_number, v]
                                    # in this section flush dataframe data to csv file
                                    total_processed_packet += 1
                                    temp_processed_packet += 1
                                    # check if csv file has been created or not
                                    if (total_processed_packet == flush_counter):
                                        processed_file_name = extracted_packet_root_dir + os.path.basename(
                                            k) + '.' + 'csv'
                                        df.to_csv(processed_file_name,index = False)
                                        # empty df dataframe
                                        # Delete the first flush_counter rows
                                        temp_processed_packet = 0
                                        has_flushed = True
                                        df = df.drop(df.index[range(flush_counter)])
                                    # csv file exist and must flush processed packet to it
                                    else:
                                        if (temp_processed_packet == flush_counter):
                                            # Write the new data to the CSV file in append mode
                                            df.to_csv(processed_file_name, mode='a', header=False, index=False)
                                            temp_processed_packet = 0
                                            # empty df dataframe
                                            # Delete the first flush_counter rows
                                            df = df.drop(df.index[range(flush_counter)])

                                # if lenght of packet is greater that MTU w must break it up to multiple packet
                                else:
                                    number_of_fragmnet_pkt = 0
                                    has_reminder = False
                                    # find number of byte in tcp header and find mtu
                                    # find tcp header
                                    p = binascii.hexlify(bytes(pkt[IP].payload)[12:13])
                                    # convert hex to binary
                                    binary_length = "{0:08b}".format(int(p, 16))
                                    # convert binary to decimal and normalize number
                                    decimal_lenght = int(binary_length, 2)
                                    numbe_of_tcp_header_byte = int(decimal_lenght / 4)
                                    mtu = default_mtu - 20 - (numbe_of_tcp_header_byte)
                                    if (int(payload_lenght % mtu) == 0):
                                        number_of_fragmnet_pkt = int(payload_lenght / mtu)
                                    else:
                                        number_of_fragmnet_pkt = int(payload_lenght / mtu) + 1
                                        has_reminder = True
                                   
                                    offset = 0
                                    new_payload = b''
                                    for index in range(number_of_fragmnet_pkt):
                                        if (has_reminder == False):
                                            new_payload += payload[offset: (index + 1) * mtu]
                                            offset += mtu
                                        else:
                                            if (index == number_of_fragmnet_pkt - 1):
                                                new_payload += payload[offset: offset + int(payload_lenght % mtu)]
                                            else:
                                                new_payload += payload[offset: (index + 1) * mtu]
                                                offset += mtu

                                        
                                        pad_len = (1500 - (int(len(new_payload) / 2) + 20 + numbe_of_tcp_header_byte))
                                        # pad_len = (1500 - int(len(new_payload)/2))
                                        pad = Padding()
                                        pad.load = '\x00' * int(pad_len)
                                        pkt = pkt / pad
                                        tcp_header = binascii.hexlify(bytes(pkt[IP].payload)[:numbe_of_tcp_header_byte])
                                        # pad_payload = binascii.hexlify(bytes(pkt[Raw].payload))
                                        pad_payload = binascii.hexlify(bytes(pad.payload))

                                        tcp_header += new_payload
                                        tcp_header += pad_payload
                                        new_payload = tcp_header
                                        ip_header = ip_masking(pkt)
                                        df.loc[len(df.index)] = [pckt_ip_source, pckt_ip_dest, pckt_src_port,
                                                                 pckt_dest_port, pckt_protocol, src_mac, dst_mac,
                                                                 pckt_ttl,
                                                                 new_payload, ip_header, packet_lenght, payload_lenght,
                                                                 pkt_number, v]
                                        new_payload = b''

                                        # in this section flush dataframe data to csv file
                                        total_processed_packet += 1
                                        temp_processed_packet += 1
                                        # check if csv file has been created or not
                                        if (total_processed_packet == flush_counter):
                                            processed_file_name = extracted_packet_root_dir + os.path.basename(
                                                k) + '.' + 'csv'
                                            df.to_csv(processed_file_name,index = False)
                                            # empty df dataframe
                                            # Delete the first flush_counter rows
                                            temp_processed_packet = 0
                                            has_flushed = True
                                            df = df.drop(df.index[range(flush_counter)])
                                        # csv file exist and must flush processed packet to it
                                        else:
                                            if (temp_processed_packet == flush_counter):
                                                # Write the new data to the CSV file in append mode
                                                df.to_csv(processed_file_name, mode='a', header=False, index=False)
                                                temp_processed_packet = 0
                                                # empty df dataframe
                                                # Delete the first flush_counter rows
                                                df = df.drop(df.index[range(flush_counter)])

                    else:
                        # if packet is a tcp packet or not
                        if pkt[IP].proto == 6 and len(res_list) == 0:
                            if pkt.haslayer(Raw):
                                src_mac = pkt[Ether].src
                                dst_mac = pkt[Ether].dst
                                pckt_ip_dest = pkt[IP].dst
                                pckt_ip_source = pkt[IP].src
                                pckt_ttl = pkt[IP].ttl
                                pckt_protocol = 'TCP'
                                pckt_dest_port = pkt[TCP].dport
                                pckt_src_port = pkt[TCP].sport
                                payload = binascii.hexlify(bytes((pkt[Raw])))
                                payload_lenght = int(len(payload) / 2)
                                packet_lenght = len(pkt)
                                # zero padding do here
                                # if (pkt[IP].len) < 1500:
                                if (len(pkt[IP])) < 1500:
                                    # find tcp header
                                    p = binascii.hexlify(bytes(pkt[IP].payload)[12:13])
                                    # convert hex to binary
                                    binary_length = "{0:08b}".format(int(p, 16))
                                    # convert binary to decimal and normalize number
                                    decimal_lenght = int(binary_length, 2)
                                    numbe_of_tcp_header_byte = int(decimal_lenght / 4)
                                    pad_len = (1500 - len(pkt[IP]))
                                    pad = Padding()
                                    pad.load = '\x00' * int(pad_len)
                                    pkt = pkt / pad
                                    tcp_header = binascii.hexlify(bytes(pkt[IP].payload)[:numbe_of_tcp_header_byte])
                                    pad_payload = binascii.hexlify(bytes(pkt[Raw]))
                                    tcp_header += pad_payload
                                    payload = tcp_header
                                    ip_header = ip_masking(pkt)
                                    df.loc[len(df.index)] = [pckt_ip_source, pckt_ip_dest, pckt_src_port,
                                                             pckt_dest_port,
                                                             pckt_protocol, src_mac, dst_mac, pckt_ttl,
                                                             payload, ip_header, packet_lenght, payload_lenght,
                                                             pkt_number, v]
                                    # in this section flush dataframe data to csv file
                                    total_processed_packet += 1
                                    temp_processed_packet += 1
                                    # check if csv file has been created or not
                                    if (total_processed_packet == flush_counter):
                                        processed_file_name = extracted_packet_root_dir + os.path.basename(
                                            k) + '.' + 'csv'
                                        df.to_csv(processed_file_name,index = False)
                                        # empty df dataframe
                                        # Delete the first flush_counter rows
                                        temp_processed_packet = 0
                                        has_flushed = True
                                        df = df.drop(df.index[range(flush_counter)])
                                    # csv file exist and must flush processed packet to it
                                    else:
                                        if (temp_processed_packet == flush_counter):
                                            # Write the new data to the CSV file in append mode
                                            df.to_csv(processed_file_name, mode='a', header=False, index=False)
                                            temp_processed_packet = 0
                                            # empty df dataframe
                                            # Delete the first flush_counter rows
                                            df = df.drop(df.index[range(flush_counter)])


                                # if lenght of packet is greater that MTU w must break it up to multiple packet
                                else:
                                    number_of_fragmnet_pkt = 0
                                    has_reminder = False
                                    # find number of byte in tcp header and find mtu
                                    # find tcp header
                                    p = binascii.hexlify(bytes(pkt[IP].payload)[12:13])
                                    # convert hex to binary
                                    binary_length = "{0:08b}".format(int(p, 16))
                                    # convert binary to decimal and normalize number
                                    decimal_lenght = int(binary_length, 2)
                                    numbe_of_tcp_header_byte = int(decimal_lenght / 4)
                                    mtu = default_mtu - 20 - (numbe_of_tcp_header_byte)
                                    if (int(payload_lenght % mtu) == 0):
                                        number_of_fragmnet_pkt = int(payload_lenght / mtu)
                                    else:
                                        number_of_fragmnet_pkt = int(payload_lenght / mtu) + 1
                                        has_reminder = True
                                    
                                    offset = 0
                                    new_payload = b''
                                    for index in range(number_of_fragmnet_pkt):
                                        if (has_reminder == False):
                                            new_payload += payload[offset: (index + 1) * mtu]
                                            offset += mtu
                                        else:
                                            if (index == number_of_fragmnet_pkt - 1):
                                                new_payload += payload[offset: offset + int(payload_lenght % mtu)]
                                            else:
                                                new_payload += payload[offset: (index + 1) * mtu]
                                                offset += mtu

                                        
                                        pad_len = (1500 - (int(len(new_payload) / 2) + 20 + numbe_of_tcp_header_byte))
                                        # pad_len = (1500 - int(len(new_payload)/2))
                                        pad = Padding()
                                        pad.load = '\x00' * int(pad_len)
                                        pkt = pkt / pad
                                        tcp_header = binascii.hexlify(bytes(pkt[IP].payload)[:numbe_of_tcp_header_byte])
                                        # pad_payload = binascii.hexlify(bytes(pkt[Raw].payload))
                                        pad_payload = binascii.hexlify(bytes(pad.payload))

                                        tcp_header += new_payload
                                        tcp_header += pad_payload
                                        new_payload = tcp_header
                                        ip_header = ip_masking(pkt)
                                        df.loc[len(df.index)] = [pckt_ip_source, pckt_ip_dest, pckt_src_port,
                                                                 pckt_dest_port, pckt_protocol, src_mac, dst_mac,
                                                                 pckt_ttl,
                                                                 new_payload, ip_header, packet_lenght, payload_lenght,
                                                                 pkt_number, v]
                                        new_payload = b''

                                        # in this section flush dataframe data to csv file
                                        total_processed_packet += 1
                                        temp_processed_packet += 1
                                        # check if csv file has been created or not
                                        if (total_processed_packet == flush_counter):
                                            processed_file_name = extracted_packet_root_dir + os.path.basename(
                                                k) + '.' + 'csv'
                                            df.to_csv(processed_file_name,index = False)
                                            # empty df dataframe
                                            # Delete the first flush_counter rows
                                            temp_processed_packet = 0
                                            has_flushed = True
                                            df = df.drop(df.index[range(flush_counter)])
                                        # csv file exist and must flush processed packet to it
                                        else:
                                            if (temp_processed_packet == flush_counter):
                                                # Write the new data to the CSV file in append mode
                                                df.to_csv(processed_file_name, mode='a', header=False, index=False)
                                                temp_processed_packet = 0
                                                # empty df dataframe
                                                # Delete the first flush_counter rows
                                                df = df.drop(df.index[range(flush_counter)])

                            

            else:
                if (pkt.haslayer(Ether) and pkt.haslayer(IP) and pkt.haslayer(UDP) and len(pkt) >= 60):
                    res_list = [i for i, value in enumerate(protocol) if
                                (pkt.haslayer(value) == True and value != 'UDP' and
                                 value != 'IP' and value != 'Ether' and value != 'Raw')]
                    if pkt[IP].proto == 17 and len(res_list) == 0:
                        if pkt.haslayer(Raw):
                            src_mac = pkt[Ether].src
                            dst_mac = pkt[Ether].dst
                            pckt_ip_dest = pkt[IP].dst
                            pckt_ip_source = pkt[IP].src
                            pckt_ttl = pkt[IP].ttl
                            pckt_protocol = 'UDP'
                            pckt_dest_port = pkt[UDP].dport
                            pckt_src_port = pkt[UDP].sport
                            payload = binascii.hexlify(bytes((pkt[Raw])))
                            payload_lenght = int(len(payload) / 2)
                            packet_lenght = len(pkt)
                            # zero padding do here
                            #if (pkt[IP].len) < 1500:
                            if (len(pkt[IP])) < 1500:
                                pad_len = (1500 - len(pkt[IP]))
                                pad = Padding()
                                pad.load = '\x00' * int(pad_len)
                                pkt = pkt / pad
                                udp_header = binascii.hexlify(bytes(pkt[IP].payload)[:8])
                                pad_payload = binascii.hexlify(bytes(pkt[Raw]))
                                udp_header += pad_payload
                                payload = udp_header
                            ip_header = ip_masking(pkt)
                            df.loc[len(df.index)] = [pckt_ip_source, pckt_ip_dest, pckt_src_port, pckt_dest_port,
                                                     pckt_protocol, src_mac, dst_mac, pckt_ttl, payload, ip_header,packet_lenght,payload_lenght,pkt_number, v]

                            # in this section flush dataframe data to csv file
                            total_processed_packet += 1
                            temp_processed_packet += 1
                            # check if csv file has been created or not
                            if (total_processed_packet == flush_counter):
                                processed_file_name = extracted_packet_root_dir + os.path.basename(k) + '.' + 'csv'
                                df.to_csv(processed_file_name,index = False)
                                # empty df dataframe
                                # Delete the first flush_counter rows
                                temp_processed_packet = 0
                                has_flushed = True
                                df = df.drop(df.index[range(flush_counter)])
                            # csv file exist and must flush processed packet to it
                            else:
                                if (temp_processed_packet == flush_counter):
                                    # Write the new data to the CSV file in append mode
                                    df.to_csv(processed_file_name, mode='a', header=False, index=False)
                                    temp_processed_packet = 0
                                    # empty df dataframe
                                    # Delete the first flush_counter rows
                                    df = df.drop(df.index[range(flush_counter)])
                            
                else:
                    pass
    
    print("finished")
    if(temp_processed_packet > 0):
        if(has_flushed == True):
            # Write the new data to the CSV file in append mode
            df.to_csv(processed_file_name, mode='a', header=False, index=False)
        else:
            processed_file_name = extracted_packet_root_dir + os.path.basename(k) + '.' + 'csv'
            df.to_csv(processed_file_name)
    return extracted_packet_root_dir