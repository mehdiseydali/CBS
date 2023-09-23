"""
The code you have provided is a function called load_pcap_datatype(). This function loads the packets from a set of pcap files, extracts the header and payload information, and saves it to a CSV file.

The function first defines a variable called root_must_normalized_dir that stores the directory where the normalized pcap files will be saved.

The function then defines a variable called normalized_files_name that stores the names of the normalized pcap files.

The function then defines a variable called chunk_size that specifies the size of the chunks that the pcap files will be broken into.

The function then loads the TLS and SSL layers.

The function then iterates over the files in the file_name_dict dictionary. For each file, the function breaks the file into chunks and saves the chunks to the root_must_normalized_dir directory.

The function then extracts the header and payload information from the packets in the normalized_files_name list and saves it to a CSV file.

The function finally returns the normalized packets.

"""
from Break_Data_File import Break_Data_File

def load_pcap_datatype(file_name_dict):

    
    normalized_files_name = []
    # must be deleted
    test_n_filename = []
    chunk_size = 40000
    load_layer("tls")
    load_layer("ssl")

    

    for k,v in file_name_dict.items():
        chunk_size_file = 10
        # get file size in MB
        size = get_file_size(k, SIZE_UNIT.BYTES)
        print('Size of file is : ', size, 'Byte')
        # breake file based on pcap size file
        if(size > 2*chunk_size_file*1024*1024 ):
            Break_Data_File(k,chunk_size_file)
        
        working_directory = os.path.splitext(os.path.basename(k))[0]
        directory = os.path.splitext(os.path.basename(k))[0]
        # Parent Directory path
        parent_dir = os.path.dirname(k)
        # Path
        path = os.path.join(parent_dir, directory)
        files = os.listdir(path)
        # in this section we show histogram of packet length
        histogram_Dataset(files,path)
        for f in files:
            print('befor reading time is :{}'.format(datetime.now().time()))
            packets = rdpcap(os.path.join(path,f))
            print('after reading time is :{}'.format(datetime.now().time()))
            print("file:{} has been read".format((os.path.join(path,f))))
            extracted_packet_root_dir = extract_header_payload_packets(packets,os.path.join(path,f) , v)
    return extracted_packet_root_dir  
