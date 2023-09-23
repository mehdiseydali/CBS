"""
The code you have provided is a function called read_pcap_files(). This function reads all the pcap files in a directory and creates a dictionary that maps the file name to the corresponding category.

The function first gets the list of all the files in the directory. It then iterates over the files and checks if the file is a pcap file. If it is, the function adds the file name and its category to the dictionary.

The function then calls the load_pcap_datatype() function to load the data from the pcap files.

Finally, the function prints the dictionary and returns it.

Here is a breakdown of the code:
"""
def read_pcap_files():
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
        if "vpn" in file_name_list[i]:
            if "chat" in file_name_list[i]:
                file_name_dict[file_name_list_full_path[i]] = 1 #"vpn chat"
            elif "email" in file_name_list[i]:
                file_name_dict[file_name_list_full_path[i]] = 3 #"vpn email"
            elif ("facebook_audio" in file_name_list[i]) or  ("hangouts_audio" in file_name_list[i])\
                        or ("skype_audio" in file_name_list[i]) or ("voip" in file_name_list[i]):
                file_name_dict[file_name_list_full_path[i]] = 5 #"vpn audio streaming"
            elif ("ftp" in file_name_list[i]) or ("file" in file_name_list[i]) \
                    or ("scp" in file_name_list[i]) or ("sftp" in file_name_list[i]):
                file_name_dict[file_name_list_full_path[i]] = 7 #"vpn ftp"
            elif ("vimeo" in file_name_list[i]) or ("youtube" in file_name_list[i]) or ("netflix" in file_name_list[i]) \
                    or ("hangouts_video" in file_name_list[i]) or ("facebook_video" in file_name_list[i]) or ("skype_video" in file_name_list[i]):
                file_name_dict[file_name_list_full_path[i]] = 9 #"vpn video streaming"
            elif "Torrent01" in file_name_list[i]:
                file_name_dict[file_name_list_full_path[i]] = 11 #"vpn p2p"
            elif "tor" in file_name_list[i]:
                file_name_dict[file_name_list_full_path[i]] = 13  # "vpn tor"
            else:
                pass
        else:
            if "chat" in file_name_list[i]:
                file_name_dict[file_name_list_full_path[i]] = 0 #"chat"
            elif "email" in file_name_list[i]:
                file_name_dict[file_name_list_full_path[i]] = 2 #"email"
            elif ("facebook_audio" in file_name_list[i]) or ("hangouts_audio" in file_name_list[i]) \
                     or ("skype_audio" in file_name_list[i]) or ("voip" in file_name_list[i]):
                file_name_dict[file_name_list_full_path[i]] = 4 #"audio streaming"
            elif ("ftp" in file_name_list[i]) or ("file" in file_name_list[i]) \
                     or ("scp" in file_name_list[i]) or ("sftp" in file_name_list[i]):
                file_name_dict[file_name_list_full_path[i]] = 6 #"ftp"
            elif ("vimeo" in file_name_list[i]) or ("youtube" in file_name_list[i]) or ("netflix" in file_name_list[i]) \
                     or ("hangouts_video" in file_name_list[i]) or ("facebook_video" in file_name_list[i]) or ("skype_video" in file_name_list[i]):
                file_name_dict[file_name_list_full_path[i]] = 8 #"video streaming"
            elif "Torrent01" in file_name_list[i]:
                file_name_dict[file_name_list_full_path[i]] = 10 #"p2p"
            elif "tor" in file_name_list[i]:
                file_name_dict[file_name_list_full_path[i]] = 14  # "tor"
            else:
                pass
    print(file_name_dict)
    load_pcap_datatype(file_name_dict)

    print('a')
    return