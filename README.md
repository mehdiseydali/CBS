# CBS
This platform is designed and implemented for encrypted traffic classification using deep learning
The general algorithm for performing classification is as follows:
1- First, the PCAP files that contain packets related to the type of traffic and application are extracted from the dataset. 
2- These PCAP files are pre-processed, which includes removing unused packets such as DNS, DHCP, etc. 
3- The important parts of the payload and header of each packet are extracted and a 1500-length record is created. This record is added to the new dataset for learning.
4- Since some types of traffic and applications in the ISCX VPN-NonVPN 2016 dataset have fewer samples than others, a GAN is used to synthesize new samples to balance the dataset.
5- Spatial features are extracted through a 1D-CNN.
6- Temporal features are extracted through an attention Bi-LSTM.
7- Statistical features are extracted through an SAE.
8- The outputs of the 1D-CNN, attention Bi-LSTM, and SAE are aggregated and fed into a fully connected network.
9- The fully connected network learns through the aggregated features and finally classifies the traffic for 12 types of traffic (e.g., email, P2P, etc.) and 17 types of applications (e.g., Skype, Vimo, etc.)


