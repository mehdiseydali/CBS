# CBS - Encrypted Traffic Classification using Deep Learning

## Overview

CBS is a platform designed and implemented for encrypted traffic classification using deep learning. The goal of this project is to accurately classify network traffic into different types and applications, such as email, P2P, Skype, and more.

## General Algorithm

The general algorithm for performing classification is as follows:

1. **Data Extraction:** PCAP files containing packets related to the type of traffic and application are extracted from the dataset.

2. **Preprocessing:** The extracted PCAP files undergo preprocessing, which includes removing unused packets such as DNS, DHCP, and other non-essential data.

3. **Feature Extraction:** Important parts of the payload and header of each packet are extracted, and a fixed-length record (e.g., 1500-length) is created. These records are added to the new dataset for learning.

4. **Data Augmentation:** To address imbalances in the dataset, especially when some traffic types have fewer samples than others, Generative Adversarial Networks (GANs) are used to synthesize new samples.

5. **Spatial Feature Extraction:** Spatial features are extracted from the data using a 1D Convolutional Neural Network (1D-CNN).

6. **Temporal Feature Extraction:** Temporal features are extracted using an attention mechanism-based Bidirectional Long Short-Term Memory (Bi-LSTM) network.

7. **Statistical Feature Extraction:** Statistical features are extracted through a Stacked Autoencoder (SAE).

8. **Feature Aggregation:** The outputs of the 1D-CNN, attention Bi-LSTM, and SAE are aggregated and fed into a fully connected neural network.

9. **Classification:** The fully connected network learns from the aggregated features and performs the final classification of traffic into 12 types of traffic (e.g., email, P2P) and 17 types of applications (e.g., Skype, Vimeo).
