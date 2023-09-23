# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from __future__ import absolute_import, division, print_function, unicode_literals

import base64
import binascii
import enum
from typing import List, Any, Union

import numpy as np
import pandas as pd
import tensorflow as tf
import tensorflow_datasets as tfds
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as mtick
from matplotlib.ticker import AutoMinorLocator
import plotly
from docutils.nodes import date
from pycodestyle import BaseReport
from pytest import collect
import os
import csv
import glob
import time
import datetime

from scapy.layers.dns import DNS
from scapy.layers.inet import IP, TCP, UDP
from scapy.layers.l2 import Ether
from scapy.layers.tls.handshake import TLSClientHello, TLSServerHello, TLSCertificateVerify
from scapy.layers.tls.handshake_sslv2 import SSLv2ClientHello, SSLv2ServerHello
from scapy.layers.tls.record import TLS
from scapy.layers.tls.record import *
from scapy.layers.tls.record_sslv2 import SSLv2
from scapy.layers.tls.record_sslv2 import *


#from scapy.layers.tls.record_sslv2 import SSLv3
from sphinx.testing.path import path
from tensorflow import keras as ks
#from tensorflow.keras.layers import la
#from keras import layers
#from keras import models

#new import for test
from tensorflow.keras import layers
from tensorflow.keras import models
#new import for test

from scipy.io import arff
from scapy.all import *
from scapy.utils import RawPcapReader
from sklearn.model_selection import train_test_split
from collections import Counter
from contextlib import redirect_stdout
import b_colors

import pktDirection

from define_FC_model_params import define_FC_model_params
from define_SAE_model_params import define_SAE_model_params
from define_Bi-LSTM_model_params import define_Bi-LSTM_model_params
from network_parameters_initializer import network_parameters_initializer
from load_pcap_datatype import load_pcap_datatype
from read_pcap_files import read_pcap_files
from packet_normalization import packet_normalization



# Enum for size units
class SIZE_UNIT(enum.Enum):
   BYTES = 1
   KB = 2
   MB = 3
   GB = 4
def convert_unit(size_in_bytes, unit):
   """ Convert the size from bytes to other units like KB, MB or GB"""
   if unit == SIZE_UNIT.KB:
       return round(size_in_bytes/1024,3)
   elif unit == SIZE_UNIT.MB:
       return size_in_bytes/(1024*1024)
   elif unit == SIZE_UNIT.GB:
       return round(size_in_bytes/(1024*1024*1024),3)
   else:
       return size_in_bytes

def get_file_size(file_name, size_type = SIZE_UNIT.BYTES ):
   """ Get file in size in given unit like KB, MB or GB"""
   size = os.path.getsize(file_name)
   return convert_unit(size, size_type)

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/


"===============================version of tensorflow and keras======================="

print("TensorFlow version: {}".format(tf.__version__))
print("Eager execution is: {}".format(tf.executing_eagerly()))
print("Keras version: {}".format(tf.keras.__version__))

"====================test on cpu or gpu ======================="
if tf.test.is_gpu_available():
    print('Running on GPU')
    print('GPU #0?')

else:
    print('Running on CPU')
print(b_colors.bcolors.warning("This is dangerous"))
my_macs = [get_if_hwaddr(i) for i in get_if_list()]
print('mac address:{}'.format(str(my_macs)))
print(Ether().src)



root_normalized_dir = 'media/mehdi/linux/normalized_data/'
sae-extracted-feature-file = 'mehdi/linux'
# in this function PCAP files read and based on file name the label extract.
extracted_packet_root_dir = read_pcap_files()
files = []
  for file in os.listdir(extracted_packet_root_dir):
    if os.path.isfile(os.path.join(extracted_packet_root_dir, file)):
      files.append(file)
# Do packet normalization
packet_normalization(files)      
# define network model parameters ( hyper parameters )
net_params = network_parameters_initializer()
#GAN model for producing syntesized data
process_csv_files()
# Define 1D-CNN the model parameters
cnn_model_params = defin_1D-CNN_model_params()
cnn_output,cnn_saved_model,cnn_saved_weights,1d-cnn_path = cnn_Traffic_classification(root_normalized_dir,net_params,cnn_model_params)
# Define Bi-LSTM the model parameters
Bi-LSTM_model_params = define_Bi-LSTM_model_params()
bi-LSTM_output,bilstm_saved_model,bilstm_saved_weights,bi-lstm_path = Bi-LSTM_Traffic_classification(root_normalized_dir,net_params,Bi-LSTM_model_params)
#Define SAE the model parameters
SAE_model_params = define_SAE_model_params()
sae_output,sae_saved_models,sae_saved_weights,sae_path = SAE_Traffic_classification(sae-extracted-feature-file,net_params,SAE_model_params)
# Combine the outputs into a single input array
fc_model_params = define_FC_model_params()
mlp_model = FC-traffic-classification(root_normalized_dir,net_params,fc_model_params, 1d-cnn_path,cnn_saved_model,bi-lstm_path,bilstm_saved_model,sae_path,sae_saved_models,sae-extracted-feature-file)












