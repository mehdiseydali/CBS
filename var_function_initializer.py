# Parameter Initialization
def var_function_initializer():
    size_list = [4,1,5,1]
    stride_list = [3,1,1,1]
    parameters_dict = {}
    parameters_dict['BATCH_SIZE'] = 64
    parameters_dict['EPOCH'] = 10
    parameters_dict['VERBOSE'] = 1
    parameters_dict['VALIDATION_SPLIT'] = 0.16
    parameters_dict['NUM_CLASSES'] = 3
    parameters_dict['OPTIMIZER'] = 'Adam'
    parameters_dict['LOSS_FUNCTION'] = 'categorical_crossentropy'
    parameters_dict['METRICS'] = ['accuracy',recall_m,precision_m,f1_m]
    parameters_dict['DROPOUT'] = 0.12
    parameters_dict['KERNEL_SIZE'] = []
    parameters_dict['FILTERS'] = 2
    parameters_dict['STRIDES'] = []
    parameters_dict['PADDING'] = 'same'
    parameters_dict['POOL_SIZE'] = (2,1)
    parameters_dict['POOL_STRIDE'] = (2,1)
    parameters_dict['HIDEN_ACTIVATION_FUNCTION'] = 'relu'
    parameters_dict['OUTPUT_ACTIVATION_FUNCTION'] = 'relu'
    parameters_dict['INPUT_SHAPE'] = (1500,1)
    parameters_dict['CNN_LAYER_SPEC'] = (2,200,200)
    parameters_dict['DENSE_LAYER'] = (2,300,200)
    parameters_dict['DENSE_LAYER_ACTIVATION_FUNCTION'] = ('relu','relu')
    parameters_dict['SOFTMAX_LAYER'] = 3
    parameters_dict['SOFTMAX_LAYER_ACTIVATION_FUNCTION'] = 'softmax'
    for i in range(parameters_dict['FILTERS']):
        parameters_dict['KERNEL_SIZE'].append(size_list[2*i])
        parameters_dict['KERNEL_SIZE'].append(size_list[2*i+1])
        parameters_dict['STRIDES'].append(stride_list[2*i])
        parameters_dict['STRIDES'].append(stride_list[2*i+1])




    return parameters_dict