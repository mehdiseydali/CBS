"""
The code you have provided is a function called packet_normalization(). This function takes a list of normalized packet files as input and normalizes the packets in each file.

The function first declares a chunk size of 50000 bytes. This is the size of each chunk that the function will break the normalized packet files into.

The function then reads the normalized packet files one by one. For each file, the function reads the payload and IP header columns.

The function then converts the payload and IP header columns from hexadecimal to binary format. It then normalizes the binary values by dividing them by 255 and multiplying them by 10 raised to the power of the decimal place.

The function then merges the header and payload columns into a single vector. It then converts the vector to a string and saves it to the packet_normalized_data column of a Pandas DataFrame.

The function then saves the Pandas DataFrame to a new file. It also breaks the new file into smaller files, each with a size of 50000 bytes.

Finally, the function returns the directory where the normalized and split files are saved.

Here is a breakdown of the code:

"""
from Break_CSV_File import Break_CSV_File
def packet_normalization(normalized_files_name):
    # declare chunk size as BYTE
    chunk_size_file = 50000

    # breake file based on pcap size file
    print('Size of file is : ', size, 'Byte')
    normalized_dir = 'media/mehdi/linux/normalized_data/'
    df_normalized = pd.DataFrame(columns=['packet_normalized_data', 'class_label'])
    binary = "{0:08b}".format(int("1a", 16))
    col_list = ["payload","ip_header", "class_label"]
    n = 2
    decPlace = 4
    payload_list = []
    header_list = []
    final_packet_vector = []
    for index1 in range(len(normalized_files_name)):

        # df = pd.read_csv("packet.csv", usecols=col_list)
        df = pd.read_csv(normalized_files_name[index1], usecols=col_list)
        print("file:{} has been read".format(normalized_files_name[index1]))
        for index, row in df.iterrows():
            print("index row is :{}".format(index))
            if(index == 65533):
                print("yes")
            payload = row["payload"].replace("'", "")[1:]
            header = row["ip_header"].replace("'", "")[1:]
            # convert hex format to binary format and binary format to decimal

            for i in range(0, len(payload), n):
                payload_list.append(payload[i:i + n])
            for j in range(0, len(header), n):
                header_list.append(header[j:j + n])
            for i in range(len(payload_list)):
                # convert hex to binary
                payload_list[i] = "{0:08b}".format(int(payload_list[i], 16))
                # convert binary to decimal and normalize number
                payload_list[i] = int(int(payload_list[i], 2) / 255.0 * 10 ** decPlace) / 10 ** decPlace
            for j in range(len(header_list)):
                # convert hex to binary
                header_list[j] = "{0:08b}".format(int(header_list[j], 16))
                # convert binary to decimal and normalize number
                header_list[j] = int(int(header_list[j], 2) / 255.0 * 10 ** decPlace) / 10 ** decPlace

            # merge header and payload to eachother
            final_packet_vector = header_list
            for data in payload_list:
                final_packet_vector.append(data)

            # convert list to string
            normalized_packet = ','.join([str(elem) for elem in final_packet_vector])
            df_normalized.loc[len(df_normalized.index)] = [normalized_packet,row["class_label"]]
            payload_list = []
            header_list = []
            final_packet_vector = []
            normalized_packet = ''
        base_filename = os.path.basename(normalized_files_name[index1])
        new_filename = normalized_dir +'normalized_'+ base_filename
        df_normalized.to_csv(new_filename)
        # in this section we break large csv file to smaller ones
        Break_CSV_File(new_filename,chunk_size_file,normalized_dir)
        df_normalized = df_normalized[0:0]
    return normalized_dir