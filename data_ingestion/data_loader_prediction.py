import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor, ExtraTreesRegressor

class Data_Getter_Pred:
    """
    This Python class is designed to load data from a source file for prediction purposes.
    It logs its actions for traceability and handles potential exceptions during the data-loading process.
    """
    def __init__(self, file_object, logger_object):
        self.prediction_file = 'Prediction_FileFromDB/InputFile.csv'
        self.file_object = file_object
        self.logger_object = logger_object

    def get_data(self):
        """
        This method reads the data from source
        """
        # Logs that the method has started
        self.logger_object.log(self.file_object, 'Entered the get_data method of the Data_Getter class')
        try:
            # Attempts to read the file at self.prediction_file using
            self.data = pd.read_csv(self.prediction_file)
            # If successful, logs the success and exits the method, returning the loaded DataFrame
            self.logger_object.log(self.file_object,
                                   'Data Load Successful. Exited the get_data method of the Data_Getter class')
            return self.data

        except Exception as e:
            self.logger_object.log(self.file_object,
                                   'Exception occurred in get_data method of the Data_Getter class. Exception message: ' + str(
                                       e))
            self.logger_object.log(self.file_object,
                                   'Data Load Unsuccessful. Exited the get_data method of the Data_Getter class')
            raise Exception()