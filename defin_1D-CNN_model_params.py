

def defin_1D-CNN_model_params():
    size_list = [4,1,5,1]
    stride_list = [3,1,1,1]
    parameters_dict = {}
    parameters_dict['DROPOUT'] = 0.12
    parameters_dict['KERNEL_SIZE'] = []
    parameters_dict['FILTERS'] = 2
    parameters_dict['STRIDES'] = []
    parameters_dict['PADDING'] = 'same'
    parameters_dict['POOL_SIZE'] = (2,1)
    parameters_dict['POOL_STRIDE'] = (2,1)
    parameters_dict['INPUT_SHAPE'] = (1500,1)
    parameters_dict['CNN_LAYER_SPEC'] = (2,200,200)
    parameters_dict['DENSE_LAYER'] = (2,300,200)
    for i in range(parameters_dict['FILTERS']):
        parameters_dict['KERNEL_SIZE'].append(size_list[2*i])
        parameters_dict['KERNEL_SIZE'].append(size_list[2*i+1])
        parameters_dict['STRIDES'].append(stride_list[2*i])
        parameters_dict['STRIDES'].append(stride_list[2*i+1])
    return parameters_dict