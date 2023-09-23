import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import savgol_filter
from google.colab import files

# Upload Excel file
uploaded = files.upload()

# Read Excel file into a DataFrame
df = pd.read_excel(next(iter(uploaded)))

# Define line styles and symbols for each column
line_styles = ['-', '--', ':']
#symbols = ['s', 'o', '^']
columns = ['CBS', 'CSCNN-[79]', 'Datanet-[19]']

# Plotting
plt.figure(figsize=(10, 6))

for i, column in enumerate(columns):
    x = df['Epoch']
    y = df[column]
    
    # Apply smoothing filter
    #y_smooth = savgol_filter(y, window_length=5, polyorder=2)
    # Apply Gaussian smoothing filter
    y_smooth = gaussian_filter1d(y, sigma=2)
    
    # Plot line with specific style and symbol
    plt.plot(x, y_smooth, linestyle=line_styles[i],linewidth=3,label=column)

# Add legend and labels
plt.legend()
plt.xlabel('Epoch')
plt.ylabel('Accuracy [%]')
# Set x-axis spacing to 2
#plt.xticks(np.arange(min(x), max(x)+1, 2))
# Set x-axis spacing to 2
plt.xticks(np.arange(min(x), 21, 1))
#plt.title('Line Plot')
# Save the plot as SVG
output_file = input("Please provide the output file name (e.g., plot.svg): ")
plt.savefig(output_file, format='svg')
print("Line plot saved as SVG.")

# Download the saved SVG file
files.download(output_file)

# Show the plot
plt.show()