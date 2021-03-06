from ..util import create_weights, create_bias

def dense_weights_creation_loop(weights_list, use_bias, weight_dtype, transpose=False):
    # Loop to create dense weights
    # In:
    #   weights_list:               list, From model configurations.py 'Dense' 'weights'
    #   use_bias:                   bool, use biases
    #   weight_dtype:               str, datatype used with weights

    # Create "connections" between every layer
    # Configurations 'weights' represents number of units in a hidden layer,
    # therefore the number of connections between layers is 'weights' list lenght - 1
    
    weights = []
    bias = []
    connections = len(weights_list)-1
    for connection in range(connections):
        if connection < connections:
            #print(connection, connections)
            
            # Define unit amounts
            in_w = weights_list[connection]
            out_w = weights_list[connection+1]

            if transpose:
                bias_num = in_w
            else:
                bias_num = out_w
            
            # Create weights
            w_var = create_weights([in_w, out_w], dtype=weight_dtype)
            
            if use_bias:
                # Create bias
                b_var = create_bias([bias_num], dtype=weight_dtype)
            else:
                b_var = None
        
            weights.append(w_var)
            bias.append(b_var)
        else:
            break

    return (weights, bias)

def dense_transpose_weights_creation_loop(weights_list, bias=None):

    weights = []
    biases = []
    for i, w in enumerate(weights_list):
        w_var = tf.transpose(w)
        if bias[i] is not None:
            b_var = bias[i]
        else:
            b_var = None
        
        weights.append(w_var)
        biases.append(b_var)

    return (weights, bias)
    
def initialize_dense_layer(
        layer_name, 
        input_dtype, 
        conf, 
        weights, 
        bias, 
        transpose
        ):
    # Create weights for the DENSE layer if not made
    # In:
    #   conf:                   dict, configuration
    # Out:
    #   (weigths, bias):        (dict, dict) modified weights dicts
    
    if not layer_name in list(weights.keys()):
        if isinstance(conf['weights'], list):
            trainable_vars = True
            # Create new weights
            cws, cbs = dense_weights_creation_loop(
                        conf['weights'], 
                        conf['use_bias'], 
                        input_dtype,
                        transpose
                        )

        elif isinstance(conf['weights'], str):
            trainable_vars = False
            # Configuration should habe the name of the layer whichs weights are used
            layer_to_reverse = conf['weights']
        
            if conf['use_bias']:
                reversed_bs = list(reversed(bias[layer_to_reverse][1]))
            else:
                reversed_bs = None

            cws, cbs = dense_transpose_weights_creation_loop(
                list(reversed(weights[layer_to_reverse][1])),
                reversed_bs,
                )
        
        weights[layer_name] = (trainable_vars, cws)
        bias[layer_name] = (trainable_vars, cbs)

    return (weights, bias)
