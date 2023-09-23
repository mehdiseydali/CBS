def cnn_build_model(parameters):
    # list out keys and values separately
    key_list = list(parameters.keys())
    val_list = list(parameters.values())
    #FILTERS = val_list[key_list.index("FILTERS")]
    KERNEL_SIZE = val_list[key_list.index("KERNEL_SIZE")]
    STRIDES = val_list[key_list.index("STRIDES")]
    PADDING = val_list[key_list.index("PADDING")]
    POOL_SIZE = val_list[key_list.index("POOL_SIZE")]
    POOL_STRIDE = val_list[key_list.index("POOL_STRIDE")]
    HIDEN_ACTIVATION_FUNCTION = val_list[key_list.index("HIDEN_ACTIVATION_FUNCTION")]
    OUTPUT_ACTIVATION_FUNCTION = val_list[key_list.index("OUTPUT_ACTIVATION_FUNCTION")]
    INPUT_DATA_SHAPE = val_list[key_list.index("INPUT_SHAPE")]
    INPUT_SHAPE =  (val_list[key_list.index("INPUT_SHAPE")][0],val_list[key_list.index("INPUT_SHAPE")][1],1)
    CNN_LAYER_SPEC = val_list[key_list.index("CNN_LAYER_SPEC")]
    DENSE_LAYER =  val_list[key_list.index("DENSE_LAYER")]
    DENSE_LAYER_ACTIVATION_FUNCTION =  val_list[key_list.index("DENSE_LAYER_ACTIVATION_FUNCTION")]
    SOFTMAX_LAYER =  val_list[key_list.index("SOFTMAX_LAYER")]
    SOFTMAX_LAYER_ACTIVATION_FUNCTION =  val_list[key_list.index("SOFTMAX_LAYER_ACTIVATION_FUNCTION")]
    
    
    model = ks.models.Sequential()
    # this CNN has been implemented based on DEEP PACKET Paper
    for i in range(CNN_LAYER_SPEC[0]):
        if i == 0 :
            model.add(ks.layers.Convolution2D(CNN_LAYER_SPEC[i+1], (KERNEL_SIZE[i],KERNEL_SIZE[i+1] ),padding=PADDING,
                                              strides=(STRIDES[i],STRIDES[i+1]),activation = HIDEN_ACTIVATION_FUNCTION, input_shape=INPUT_SHAPE))
        else:

            model.add(ks.layers.Convolution2D(CNN_LAYER_SPEC[i+1],(KERNEL_SIZE[2*i],KERNEL_SIZE[2*i+1] ) ,padding = PADDING,
                                              strides=(STRIDES[2*i],STRIDES[2*i+1]),activation=HIDEN_ACTIVATION_FUNCTION))

    model.add(ks.layers.MaxPooling2D(pool_size= (POOL_SIZE[0],POOL_SIZE[1]), strides= (POOL_STRIDE[0],POOL_STRIDE[1])))
    # Flatten => RELU layers
    model.add(ks.layers.Flatten())
    # Dense Connected Layer
    for i in range(DENSE_LAYER[0]):
        model.add(ks.layers.Dense(DENSE_LAYER[i+1], activation=DENSE_LAYER_ACTIVATION_FUNCTION[i]))
        
   
    
    return model