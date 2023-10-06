def BiLSTM_build_model(params):

   
  # Define the model architecture
  model = tf.keras.Sequential()

  # Add the Bi-LSTM layers
  model.add(tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(params['input_shape'][1], return_sequences=True), input_shape=params['input_shape']))
  model.add(tf.keras.layers.BatchNormalization())
  model.add(tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(params['input_shape'][1], return_sequences=True)))
  model.add(tf.keras.layers.BatchNormalization())
  model.add(tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(params['input_shape'][1], return_sequences=True)))
  model.add(tf.keras.layers.BatchNormalization()) 

  # Add the attention layer
  model.add(tf.keras.layers.Attention())

  # Add the fully connected layers (MLP)
  model.add(tf.keras.layers.Dense(params['dense_neurons'][0], activation=params['activation']))
  model.add(tf.keras.layers.BatchNormalization())
  model.add(tf.keras.layers.Dense(params['dense_neurons'][1], activation=params['activation']))
  model.add(tf.keras.layers.BatchNormalization())
  model.add(tf.keras.layers.Dense(params['dense_neurons'][2], activation=params['activation']))
  model.add(tf.keras.layers.BatchNormalization()) 
  model.add(tf.keras.layers.Dense(params['dense_neurons'][3], activation=params['activation']))
  model.add(tf.keras.layers.BatchNormalization())  
  # Save the model
  model.save('bilstm_model.h5')
   
  return model
