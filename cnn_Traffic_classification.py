# in this function we build CNN for Traffic Classification
import time
from cnn_build_model import cnn_build_model
def cnn_Traffic_classification(root_normalized_dir,net_parameters,model_parameters):
    # Record the start time
    start_time = time.time()
    df_normalized = pd.DataFrame(columns=['packet_normalized_data', 'class_label'])
    df_train = pd.DataFrame(columns=['packet_normalized_data'])
    binary = "{0:08b}".format(int("1a", 16))
    col_list = ['packet_normalized_data', 'class_label']
    
    # list out keys and values separately
    key_list = list(net_parameters.keys())
    val_list = list(net_parameters.values())
    
    # list out keys and values separately
    key_list1 = list(model_parameters.keys())
    val_list1 = list(model_parameters.values())
    DENSE_LAYER =  val_list1[key_list1.index("DENSE_LAYER")]
    
    # network parameters
    BATCH_SIZE = val_list[key_list.index("BATCH_SIZE")]
    EPOCH = val_list[key_list.index("EPOCH")]
    VERBOSE =  val_list[key_list.index("VERBOSE")]
    #OPTIMIZER = tf.keras.optimizers.Adam()
    VALIDATION_SPLIT = val_list[key_list.index("VALIDATION_SPLIT")]
    NUM_CLASSES = val_list[key_list.index("NUM_CLASSES")]
    OPTIMIZER = val_list[key_list.index("OPTIMIZER")]
    LOSS_FUNCTION = val_list[key_list.index("LOSS_FUNCTION")]
    METRICS =  val_list[key_list.index("METRICS")[0], key_list.index("METRICS")[1](),key_list.index("METRICS")[2](),key_list.index("METRICS")[3]()]
    DROPOUT = val_list[key_list.index("DROPOUT")]

    for path in os.listdir(root_normalized_dir):
        full_path = os.path.join(root_normalized_dir, path)
        df = pd.read_csv(full_path, usecols=col_list)
        model = cnn_build_model(model_parameters)
        model.compile(loss=LOSS_FUNCTION,
                      optimizer=OPTIMIZER,
                      metrics=METRICS)
        model.summary()
        print("this is running 1D-CNN model: ")

        # train on model
        X = df.iloc[:,0:1] # Data
        Y =  df.iloc[:,1:2]  # Label
        X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)
        # prepare label of packet for deep NN
        train_label_data_list = []
        test_label_data_list = []
        pkt_train_label_data = np.zeros([len(y_train), 1])
        pkt_test_label_data = np.zeros([len(y_test), 1])
        for i in range(len(y_train)):
            pkt_train_label_data[i,0] = y_train.iloc[i,0]
        #train_label_data_list.append(pkt_train_label_data)
        train_label = np.array(pkt_train_label_data)
        train_label = train_label[:,0]
        train_label = train_label.astype(np.int)
        for i in range(len(y_test)):
            pkt_test_label_data[i,0] = y_test.iloc[i,0]
        #test_label_data_list.append(pkt_test_label_data)
        test_label = np.array(pkt_test_label_data)
        test_label = test_label[:, 0]
        test_label = test_label.astype(np.int)

        #y_train = y_train.to_numpy()
        #y_train = y_train.T
        # To create a x-by-y-by-z 3D list with initial values:
        
        data_list = []
        test_list = []

        pkt_data = np.zeros([len(X_train.iloc[0, 0].split(',')), 1])
        for i in range(len(X_train)):
            print("trian preparing data i {}".format(i))
            pkt_train_data = np.zeros([len(X_train.iloc[0, 0].split(',')), 1])
            temp_train_list = X_train.iloc[i, 0].split(',')[:]
            for j in range(len(temp_train_list)):
                #print("test preparing data j {}".format(j))
                pkt_train_data[j,0] = float(temp_train_list[j])
            data_list.append(pkt_train_data)
            
        train_data = np.array(data_list)
        for i in range(len(X_test)):
            print("test preparing data i {}".format(i))
            pkt_test_data = np.zeros([len(X_test.iloc[0, 0].split(',')), 1])
            temp_test_list = X_test.iloc[i, 0].split(',')[:]
            for j in range(len(temp_test_list)):
                #print("test preparing data j {}".format(j))
                pkt_test_data[j,0] = float(temp_test_list[j])
            test_list.append(pkt_test_data)
        test_data = np.array(test_list)
        # convert class vectors to binary class matrices
        train_label = tf.keras.utils.to_categorical(train_label, NUM_CLASSES)
        test_label = tf.keras.utils.to_categorical(test_label, NUM_CLASSES)
        
        train_data = train_data.reshape((len(train_data), len(X_train.iloc[0,0].split(',')), 1, 1))
        test_data = test_data.reshape((len(test_data), len(X_test.iloc[0, 0].split(',')), 1, 1))
        #model = create_1dcnn_model()
        
               
        model.fit(train_data, train_label, batch_size=BATCH_SIZE,
                  epochs=EPOCH,verbose=VERBOSE,validation_split= VALIDATION_SPLIT )
        #score = model.evaluate(test_data, test_label,
        #                       batch_size=BATCH_SIZE)
        (loss, accuracy, f1_score, precision, recall) = model.evaluate(test_data, test_label,
                               batch_size=BATCH_SIZE)
        score = []
        score[0] = loss
        score[1]= accuracy
        score[2] = f1_score
        score[3] = precision
        score[4] = recall
        
        print("\nTest loss:", score[0])
        print('Test accuracy:', score[1])
        print('Test f1_score:', score[2])
        print('Test precision:', score[3])
        print('Test recall:', score[4])
        
    saved_models = []
    saved_weights = []    
    save_model_weights_dir = 'media/mehdi/linux/normalized_data/'
    # save model architecture    
    model.save(save_model_weights_dir + 'model_architecture_cnn.h5')
    saved_models.append(save_model_weights_dir +'model_architecture_cnn.h5')
    # save model weights
    model.save_weights('model_weights_cnn.h5')     
    saved_weights.append('model_weights_cnn.h5')
    # Get the output of the last connected layer
    last_dense_output = model.layers[-DENSE_LAYER[0]].output   
    # Record the end time
    end_time = time.time()
    # Calculate the execution time in seconds
    execution_time = end_time - start_time

    # Convert execution time to minutes for better readability
    execution_time_minutes = execution_time / 60

    print(f"GAN training completed in {execution_time:.2f} seconds ({execution_time_minutes:.2f} minutes).") 
    return last_dense_output,saved_models,saved_weights,save_model_weights_dir  
