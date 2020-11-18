from . import create_prediction_file, run_function, map_params, test_functions, fetch_model, get_dataset_info

class ModelHandler:
    # Necessary ?

    def __init__(self, dataset, model_name, conf_name):
        if dataset is not None:
            self.training_dataset = dataset[0]
            self.test_dataset = dataset[1]
        
        self.model = fetch_model(model_name, conf_name)

    def train(self, params):
        # Training function
        # Takes predefined training dataset and feeds data to the models training function
        # In:
        #   params:                     Namespace object

        command_params = vars(params)
        command_params['dataset'] = self.training_dataset
        self.model.train(**map_params(self.model.train, command_params, self.model.c))

    def test(self, test_type=None, results=None, train=False):
        # Test function
        # Uses result.json from models outputs to run tests on the dataset
        # In:
        #   test_type:                  str, name of the function in test_functions
        #   results:                    dict, key = label, value = numpy array of model outputs
        #   train:                      bool, True to use training_dataset instead of test

        if results is None:
            #Create label model output dict and save it
            path = self.model.load_path
            #print(path)
            if train:
                dataset = self.training_dataset
            else:
                dataset = self.test_dataset
            
            results = create_prediction_file(path, dataset, self.model, train=train)
        
        for label, result in results.items():
            print(label, ": ",result.shape)
        
        if test_type is not None:
            run_function(test_functions, test_type, {'results':results, 'model':self.model})
