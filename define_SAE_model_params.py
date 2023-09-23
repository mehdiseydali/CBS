def define_SAE_model_params():
    encoder_neurons_sae1 = []
    code_neurons_sae1 = []
    decoder_neurons_sae1 = []
    output_neurons_sae1 = [20, 15, 10, 15, 10, 20]

    for _ in range(6):
        encoder_neurons_sae.append([1024, 512, 256, 128])
        code_neurons_sae.append(10)
        decoder_neurons_sae.append([128, 256, 512, 1024])

    dictionary = {
        'encoder_neurons_sae': encoder_neurons_sae1,
        'code_neurons_sae': code_neurons_sae1,
        'decoder_neurons_sae': decoder_neurons_sae1,
        'output_neurons_sae': output_neurons_sae1
    }

    return dictionary