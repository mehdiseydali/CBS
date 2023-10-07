import os
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.layers import Conv1D, MaxPooling1D, Flatten, Dense, Reshape, BatchNormalization, LeakyReLU
from tensorflow.keras.models import Sequential


# Define the Generator model
def build_generator(latent_dim):
    
    generator = tf.keras.Sequential()
    generator.add(layers.Conv1D(256, kernel_size=3, activation=tf.keras.layers.LeakyReLU(), input_shape=(1, 1500), input_dim=latent_dim))
    generator.add(layers.BatchNormalization())
    generator.add(layers.AveragePooling1D(pool_size=2, strides=2))
    generator.add(layers.Conv1D(128, kernel_size=3, activation=tf.keras.layers.LeakyReLU()))
    generator.add(layers.BatchNormalization())
    generator.add(layers.AveragePooling1D(pool_size=2, strides=2))
    generator.add(layers.Conv1D(64, kernel_size=3, activation=tf.keras.layers.LeakyReLU()))
    generator.add(layers.BatchNormalization())
    generator.add(layers.AveragePooling1D(pool_size=2, strides=2))
    generator.add(layers.Flatten())
    generator.add(layers.Dense(1500, activation='tanh')
    generator.add(layers.Reshape((1, 1500)))
    return generator


# Define the Discriminator model
def build_discriminator():
    discriminator = tf.keras.Sequential()
    discriminator.add(layers.Conv1D(256, kernel_size=3, activation=tf.keras.layers.LeakyReLU(), input_shape=(1, 1500)))
    discriminator.add(layers.BatchNormalization())
    discriminator.add(layers.AveragePooling1D(pool_size=2, strides=2))
    discriminator.add(layers.Conv1D(128, kernel_size=3, activation=tf.keras.layers.LeakyReLU()))
    discriminator.add(layers.BatchNormalization())
    discriminator.add(layers.AveragePooling1D(pool_size=2, strides=2))
    discriminator.add(layers.Conv1D(64, kernel_size=3, activation=tf.keras.layers.LeakyReLU()))
    discriminator.add(layers.BatchNormalization())
    discriminator.add(layers.AveragePooling1D(pool_size=2, strides=2))
    discriminator.add(layers.Flatten())
    discriminator.add(layers.Dense(1, activation='sigmoid'))
    return discriminator


# Combine the Generator and Discriminator into a GAN model
def build_gan(generator, discriminator):
    discriminator.trainable = False
    model = Sequential()
    model.add(generator)
    model.add(discriminator)
    return model


# Load the CSV files from the directory
def load_csv_files(directory):
    csv_files = [file for file in os.listdir(directory) if file.endswith('.csv')]
    dataframes = []
    for file in csv_files:
        dataframe = pd.read_csv(os.path.join(directory, file))
        dataframes.append(dataframe)
    return dataframes


# Generate artificial data using GAN for specific labels
def generate_artificial_data(generator, num_samples):
    latent_dim = 100
    noise = np.random.normal(0, 1, (num_samples, latent_dim))
    artificial_data = generator.predict(noise)
    return artificial_data


# GAN model network program
def process_csv_files()
    directory = './data'  # Directory containing the CSV files
    num_samples = int(input("Enter the number of samples to generate via GAN: "))

    # Load CSV files
    dataframes = load_csv_files(directory)

    # Process each CSV file
    for dataframe in dataframes:
        packet_data = dataframe['packet_normalized_data'].values
        class_labels = dataframe['class_label'].values

        # Filter class labels requiring artificial data
        labels_to_generate = [0, 2, 3, 11]
        filtered_indices = [i for i, label in enumerate(class_labels) if label in labels_to_generate]
        filtered_packet_data = packet_data[filtered_indices]
        filtered_class_labels = class_labels[filtered_indices]

        # Prepare and train GAN only if there are filtered records
        if len(filtered_indices) > 0:
            # Prepare data for GAN training (Normalize between -1 and 1)
            filtered_packet_data = (filtered_packet_data - np.min(filtered_packet_data)) / (
                    np.max(filtered_packet_data) - np.min(filtered_packet_data))
            filtered_packet_data = 2 * filtered_packet_data - 1
            filtered_packet_data = np.expand_dims(filtered_packet_data, axis=-1)

            # Build and compile the models
            generator = build_generator(latent_dim=100)
            discriminator = build_discriminator()
            gan = build_gan(generator,discriminator)

            discriminator.compile(loss='binary_crossentropy', optimizer='adam')
            gan.compile(loss='binary_crossentropy', optimizer='adam')

            # Train the GAN
            batch_size = 32
            epochs = 100
            num_batches = len(filtered_packet_data) // batch_size

            for epoch in range(epochs):
                for batch in range(num_batches):
                    # Select a random batch of real samples
                    real_samples = filtered_packet_data[batch * batch_size:(batch + 1) * batch_size]

                    # Generate a batch of fake samples
                    noise = np.random.normal(0, 1, (batch_size, latent_dim))
                    fake_samples = generator.predict(noise)

                    # Train the discriminator
                    discriminator.trainable = True
                    d_loss_real = discriminator.train_on_batch(real_samples, np.ones((batch_size, 1)))
                    d_loss_fake = discriminator.train_on_batch(fake_samples, np.zeros((batch_size, 1)))
                    d_loss = 0.5 * np.add(d_loss_real, d_loss_fake)

                    # Train the generator
                    discriminator.trainable = False
                    g_loss = gan.train_on_batch(noise, np.ones((batch_size, 1)))

                # Print the progress
                print(f"Epoch {epoch + 1}/{epochs} - D loss: {d_loss} - G loss: {g_loss}")

            # Generate artificial data
            artificial_data = generate_artificial_data(generator, num_samples)

            # Add the artificial data to the original dataframe
            dataframe = dataframe.append(pd.DataFrame({
                'packet_normalized_data': artificial_data.squeeze(),
                'class_label': np.random.choice(labels_to_generate, num_samples)
            }), ignore_index=True)

            # Save the updated dataframe back to the original CSV file
            dataframe.to_csv(os.path.join(directory, file), index=False)
=============================================================================================================
