def define_Bi-LSTM_model_params():
    # Define the model parameters as a dictionary
    params = {
        'input_shape': (1, 1500),  # Shape of input data [1*1500]
        'activation': 'relu',  # Activation function for the fully connected layers
        'dense_neurons': [1024, 512, 256, 74]  # Number of neurons in each dense layer
    }
    return params