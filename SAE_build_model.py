import tensorflow as tf
from tensorflow.keras import layers
import pandas as pd
    
def SAE_build_moel(params,net_parameters,train_data,test_data,train_label,test_label,LOSS_FUNCTION,OPTIMIZER,METRIC):

    encoder_neurons_sae = params['encoder_neurons_sae']
    code_neurons_sae = params['code_neurons_sae']
    decoder_neurons_sae = params['decoder_neurons_sae']
    output_neurons_sae = params['output_neurons_sae'] 
    autoencoders = []  # Create an empty list to store the output of define_autoencoder
    # list out keys and values separately
    key_list = list(net_parameters.keys())
    val_list = list(net_parameters.values())
    # network parameters
    BATCH_SIZE = val_list[key_list.index("BATCH_SIZE")]
    EPOCH = val_list[key_list.index("EPOCH")]
    VERBOSE =  val_list[key_list.index("VERBOSE")]
    #OPTIMIZER = tf.keras.optimizers.Adam()
    VALIDATION_SPLIT = val_list[key_list.index("VALIDATION_SPLIT")]
    #NUM_CLASSES = val_list[key_list.index("NUM_CLASSES")]
    OPTIMIZER = val_list[key_list.index("OPTIMIZER")]
    LOSS_FUNCTION = val_list[key_list.index("LOSS_FUNCTION")]
    METRICS =  val_list[key_list.index("METRICS")[0], key_list.index("METRICS")[1](),key_list.index("METRICS")[2](),key_list.index("METRICS")[3]()]
    DROPOUT = val_list[key_list.index("DROPOUT")]
    stack = []
    
    # Process each parameter individually
    for i in range(6):
        encoder_neurons = encoder_neurons_sae[i]
        code_neurons = code_neurons_sae[i]
        decoder_neurons = decoder_neurons_sae[i]
        output_neurons = output_neurons_sae[i]
        # Call the autoencoder function with each set of parameters
        autoencoder = define_autoencoder(encoder_neurons, code_neurons, decoder_neurons, output_neurons)
        autoencoders.append(autoencoder)  # Append the output to the list
    for model in autoencoders:
        model.compile(loss=LOSS_FUNCTION,
                      optimizer=OPTIMIZER,
                      metrics=METRICS)
        model.summary()
        if(autoencoders.index(model) == 1):
            stack.append([autoencoders.index(model)]) = model.fit(train_data, train_data, batch_size=BATCH_SIZE,
                  epochs=EPOCH,verbose=VERBOSE, validation_data=(test_data, test_data) )
        else:
            temp_input = model.predict(train_data)
            temp_input = np.concatenate((temp_input , train_data))  
            stack.append([autoencoders.index(model)]) = model.fit(temp_input, temp_input, batch_size=BATCH_SIZE,
                  epochs=EPOCH,verbose=VERBOSE, validation_data=(test_data, test_data) )    
            train_data = temp_input       
    return stack, stack[6].get_layer('code').output) 