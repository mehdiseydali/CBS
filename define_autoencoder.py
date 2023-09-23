import tensorflow as tf
from tensorflow.keras import layers
import pandas as pd

def define_autoencoder(input_shape, encoder_neurons, code_neurons, decoder_neurons, output_neurons):
    # Encoder
    input_data = tf.keras.Input(shape=input_shape, name='input')
    encoder = input_data
    for neurons in encoder_neurons:
        encoder = layers.Dense(neurons, activation='relu')(encoder)

    # Code layer
    code = layers.Dense(code_neurons, activation='relu', name='code')(encoder)

    # Decoder
    decoder = code
    for neurons in decoder_neurons:
        decoder = layers.Dense(neurons, activation='relu')(decoder)

    # Output layer
    output = layers.Dense(output_neurons, name='output')(decoder)

    # Define the model
    model = tf.keras.Model(inputs=input_data, outputs=output)
    return model