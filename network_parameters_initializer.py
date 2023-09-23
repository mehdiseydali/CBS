def network_parameters_initializer():
    
    network_parameters_dict = {}
    network_parameters_dict['BATCH_SIZE'] = 64
    network_parameters_dict['LEARNING_RATE'] = 0.0001
    network_parameters_dict['EPOCH'] = 50
    network_parameters_dict['VERBOSE'] = 1
    network_parameters_dict['VALIDATION_SPLIT'] = 0.1
    network_parameters_dict['NUM_CLASSES'] = 3
    network_parameters_dict['OPTIMIZER'] = 'Adam'
    network_parameters_dict['LOSS_FUNCTION'] = 'categorical_crossentropy'
    network_parameters_dict['METRICS'] = ['accuracy',recall_m,precision_m,f1_m]
    network_parameters_dict['DROPOUT'] = 0.30
    network_parameters_dict['HIDEN_ACTIVATION_FUNCTION'] = 'relu'
    network_parameters_dict['OUTPUT_ACTIVATION_FUNCTION'] = 'relu'
    network_parameters_dict['DENSE_LAYER_ACTIVATION_FUNCTION'] = ('relu','relu')
    network_parameters_dict['SOFTMAX_LAYER_ACTIVATION_FUNCTION'] = 'softmax'
    
    return network_parameters_dict
