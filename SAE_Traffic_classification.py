# in this function we build CNN for Traffic Classification
def SAE_Traffic_classification(sae_feature_dir,net_parameters,model_params):
    
    df_normalized = pd.DataFrame(columns=['sae_normalized_features', 'class_label'])
    df_train = pd.DataFrame(columns=['sae_normalized_features'])
    binary = "{0:08b}".format(int("1a", 16))
    col_list = ['sae_normalized_features', 'class_label']
    

    

    for path in os.listdir(sae_feature_dir):
        
        full_path = os.path.join(sae_feature_dir, path)
        df = pd.read_csv(full_path, usecols=col_list)
        
        # train on model
        X = df.iloc[:,0:1] # Data
        Y =  df.iloc[:,1:2]  # Label
        X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)
        # prepare label of packet for deep NN
        train_label_data_list = []
        test_label_data_list = []
        train_label_data = np.zeros([len(y_train), 1])
        test_label_data = np.zeros([len(y_test), 1])
        for i in range(len(y_train)):
            train_label_data[i,0] = y_train.iloc[i,0]
        #train_label_data_list.append(pkt_train_label_data)
        train_label = np.array(train_label_data)
        train_label = train_label[:,0]
        train_label = train_label.astype(np.int)
        for i in range(len(y_test)):
            test_label_data[i,0] = y_test.iloc[i,0]
        #test_label_data_list.append(pkt_test_label_data)
        test_label = np.array(test_label_data)
        test_label = test_label[:, 0]
        test_label = test_label.astype(np.int)
        # convert class vectors to binary class matrices
        train_label = tf.keras.utils.to_categorical(train_label, NUM_CLASSES)
        test_label = tf.keras.utils.to_categorical(test_label, NUM_CLASSES)
        
        train_data = train_data.reshape((len(train_data), len(X_train.iloc[0,0].split(',')), 1, 1))
        test_data = test_data.reshape((len(test_data), len(X_test.iloc[0, 0].split(',')), 1, 1))
        stack_autoencoder_list,code_layer_output = SAE_build_model(model_params,net_parameters,train_data,test_data,train_label,test_label,LOSS_FUNCTION,OPTIMIZER,METRICS)
         

        

        
    saved_models = []
    saved_weights = []
    save_model_weights_dir = 'media/mehdi/linux/normalized_data/'
    for i, model in enumerate(stack_autoencoder_list):
        # save model architecture 
        tf.keras.models.save_model(model, save_model_weights_dir + f'model_architecture_sae{i}.h5')
        saved_models.append(f'model_architecture_sae{i}.h5')
        tf.keras.models.save_weights(model, save_model_weights_dir + f'model_weights_sae{i}.h5')
        saved_weights.append(f'model_weights_sae{i}.h5')
        # save model weights
    return code_layer_output,save_models,saved_weights, save_model_weights_dir     