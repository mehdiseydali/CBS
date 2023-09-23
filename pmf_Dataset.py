"""
The code you have provided is a function called pmf_Dataset(). This function calculates the probability mass function (PMF) of the packet lengths in a set of CSV files.

The function first defines a list called csv_files that stores the names of the CSV files in the specified directory.

The function then defines a list called my_temp_list that stores the number of packets in each length range. The my_packet_length_list list is initialized with 0s.

The function then iterates over the csv_files list. For each CSV file, the function reads the file and stores the number of packets in each length range in the my_temp_list list.

The function then calculates the PMF of the packet lengths by dividing the number of packets in each length range by the total number of packets.

The function finally returns the PMF of the packet lengths.

The first few lines define the csv_files list and the my_temp_list list.

The next few lines iterate over the csv_files list. For each CSV file, the function reads the file and stores the number of packets in each length range in the my_temp_list list.

The next few lines calculate the PMF of the packet lengths by dividing the number of packets in each length range by the total number of packets.

The final few lines format the PMF as strings and return it.

"""

def pmf_Dataset(rootDir):
    csv_files = os.listdir(rootDir)
    my_temp_list = []
    my_packet_length_list = [0]*9
    my_packet_length_list = [float(x) for x in my_packet_length_list]
    # loop over the list of csv files
    for f in csv_files:
        # read the csv file
        path = os.path.join(rootDir, f)
        df = pd.read_csv(path,usecols=['Topic / Item','Count'])

        # print the location and filename
        print('Location:', path)
        df_percent= df.iloc[1:10,1:2]
        my_temp_list = df_percent['Count'].values.tolist()
        for item in range(len(my_temp_list)):
            #my_temp_list[item] = str(my_temp_list[item]).replace("%","")
            my_packet_length_list[item] = my_packet_length_list[item] + my_temp_list[item]
        print(my_temp_list)
        # print the content
        print('Content:')
        print(df)
        print()
    total_packet = sum(my_packet_length_list)
    packet_lenght_percent = [(float(x/total_packet)*100) for x in my_packet_length_list]
    print(packet_lenght_percent)
    final_packet_lenght = ['{:.2f}'.format(x) for x in packet_lenght_percent]

    return