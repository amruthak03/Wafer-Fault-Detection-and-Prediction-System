import pandas as pd

class Data_Getter:
    """
    This class is designed to fetch data from a specified source (in this case, a CSV file) and return it as a pandas
    DataFrame. The class uses logging to track its operations and handle any exceptions that may occur.
    """
    def __init__(self, file_object, logger_object):
        self.training_file = 'Training_FileFromDB/InputFile.csv'
        self.file_object = file_object
        self.object = logger_object
        self.logger_object = self.object

    def get_data(self):
        """
        Reads the data from the specified file and returns it as a pandas DataFrame.
        """
        # Logs that the get_data method has started
        self.logger_object.log(self.file_object, 'Entered the get_data method of the Data_Getter class.')
        try:
            # Load and read the CSV file
            self.data = pd.read_csv(self.training_file)
            # If data is successfully loaded, logs the success and returns the DataFrame
            self.logger_object.log(self.file_object,
                                   'Data Load Successful. Exited the get_data method of the Data_Getter class.')

            return self.data

        except Exception as e:
            self.logger_object.log(self.file_object,
                                   'Exception occurred in get_data method of the Data_Getter class. Exception message: '
                                   + str(e))
            self.logger_object.log(self.file_object,
                                   'Data Load Unsuccessful. Exited the get_data method of the Data_Getter class')
            raise Exception()
