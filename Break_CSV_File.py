
"""
The code you have provided is a function called Break_CSV_File(). This function breaks a large CSV file into smaller files of a specified size.

The function first creates a list to store the number of rows in each chunk.

The function then iterates over the CSV file in chunks of the specified size. For each chunk, the function adds the number of rows in the chunk to the list.

If the number of chunks is greater than or equal to 2, then the function breaks the CSV file into smaller files. The function creates a new file for each chunk and writes the chunk to the file.

The function also removes the original CSV file.

The first line defines the chunks_list variable to store the number of rows in each chunk.

The next line defines the normalized_dir variable as the directory where the broken CSV files will be saved.

The next line iterates over the CSV file in chunks of the specified size. For each chunk, the function adds the number of rows in the chunk to the chunks_list variable.

The next line checks if the number of chunks is greater than or equal to 2. If it is, then the function breaks the CSV file into smaller files.

The next few lines create a new file for each chunk and writes the chunk to the file.

The last line removes the original CSV file.
"""

def Break_CSV_File(filename,chunk_size,normalized_dir):
    chunks_list = []
    #normalized_dir = 'media/mehdi/linux/normalized_data/'
    for chunk in pd.read_csv(filename, iterator=True, chunksize=chunk_size):
        chunks_list.append(len(chunk))
    if(len(chunks_list) >=2):
        base_filename = os.path.basename(filename)
        for i, chunk in enumerate(pd.read_csv(filename, chunksize=chunk_size)):
            chunk.to_csv(normalized_dir + base_filename +'_chunk' + '{}'.format(i), index=False)
        if os.path.exists(normalized_dir+os.path.basename(filename)):
            os.remove(normalized_dir+os.path.basename(filename))
            print("file with name {} has been chunked and rermoved ".format(base_filename))
    return