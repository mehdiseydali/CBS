"""
The code you have provided is a function called Break_Data_File(). This function breaks a large pcap file into smaller files of a specified size.

The function first creates a directory with the same name as the pcap file. If the directory already exists, then the function deletes all the files in the directory.

The function then creates a tcpdump script that breaks the pcap file into smaller files of the specified size. The tcpdump script is executed using the os.system() function.

The function also creates an editcap script that can be used to further break the pcap files into smaller files. However, the editcap script is not executed by the function.

The first line defines the directory variable as the name of the directory that will be created to store the broken pcap files. The parent_dir variable is the parent directory of the pcap file. The path variable is the full path to the directory that will be created.

The next four lines check if the directory directory exists. If it does not exist, then the function creates the directory. If the directory does exist, then the function deletes all the files in the directory.

The next line defines the tcpdump_script variable as the tcpdump script that will be used to break the pcap file into smaller files. The editcap_script variable is defined as the editcap script that can be used to further break the pcap files into smaller files.

The next line defines the new_filename variable as the name of the broken pcap file. The saved_break_file variable is the full path to the broken pcap file.

The next line executes the tcpdump_script using the os.system() function.

The last line commented out executes the editcap_script using the os.system() function.
"""

def Break_Data_File(filename,chunk_size):
    # create a floder as name as file for breaked files
    # Directory
    directory = os.path.splitext(os.path.basename(filename))[0]
    # Parent Directory path
    parent_dir = os.path.dirname(filename)
    # Path
    path = os.path.join(parent_dir, directory)
    # Create the directory
    if(os.path.isdir(path) == False):
        os.mkdir(path)
    else:
        for f in os.listdir(path):
            os.remove(os.path.join(path, f))
    print("Directory '% s' created" % directory)
    # in this section large file greater than chunk size will be breake
    tcpdump_script = ""
    editcap_script = ""
    #new_dir_filename = os.path.dirname(filename)
    new_filename = "breaked_" + os.path.splitext(os.path.basename(filename))[0]
    #saved_break_file = new_dir_filename + "/" + new_filename
    saved_break_file = path + "/" + new_filename
    tcpdump_script = "tcpdump -r " + filename + " -w " + saved_break_file + " -C " + str(chunk_size)
    editcap_script = "editcap -c 100000 " + filename + " " + saved_break_file
    os.system(tcpdump_script)
    # os.system(editcap_script)

