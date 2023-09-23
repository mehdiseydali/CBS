def fc_build_model(params):
    
    model = Sequential()
  
    # First layer
    model.add(Dense(params['first_layer'], input_shape=(params['input_shape'],)))
    model.add(Dropout(params['dropout_rate']))
    model.add(BatchNormalization())
  
    # Second layer
    model.add(Dense(params['second_layer'], activation='relu'))
    model.add(Dropout(params['dropout_rate']))
    model.add(BatchNormalization())
  
    # Third layer
    model.add(Dense(params['third_layer'], activation='relu'))
    model.add(Dropout(params['dropout_rate']))
    model.add(BatchNormalization())
  
    # Fourth layer
    model.add(Dense(params['fourth_layer'], activation='relu'))
    model.add(Dropout(params['dropout_rate']))
    model.add(BatchNormalization())
  
    # Last layer
    if params['num_classes'] == 12:
        output_units = 12
    elif params['num_classes'] == 17:
        output_units = 17
    else:
        raise ValueError("Invalid number of classes!")
        
    model.add(Dense(output_units, activation='softmax'))
    # Compile the model
    #model.compile(optimizer=params['optimizer'], loss=params['loss_function'])

    return model 