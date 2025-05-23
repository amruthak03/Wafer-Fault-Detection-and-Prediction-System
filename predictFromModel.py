import pandas as pd
from file_operations import file_methods
from data_preprocessing import preprocessing
from data_ingestion import data_loader_prediction
from application_logging import logger
from Prediction_Raw_Data_Validation.predictionDataValidation import Prediction_Data_validation

class prediction:
    """
    This script represents the entry point for predicting a machine learning model using a structured pipeline.
    """
    def __init__(self, path):
        self.file_object = open("Prediction_Logs/Prediction_Log.txt", 'a+')
        self.log_writer = logger.App_Logger()
        if path is not None:
            self.pred_data_val = Prediction_Data_validation(path)

    def predictionFromModel(self):
        try:
            # Delete the existing prediction file from last run!
            self.pred_data_val.deletePredictionFile()
            self.log_writer.log(self.file_object, 'Start of Prediction')
            # Getting the data
            data_getter = data_loader_prediction.Data_Getter_Pred(self.file_object, self.log_writer)
            data = data_getter.get_data()

            # Data Preprocessing
            preprocessor = preprocessing.Preprocessor(self.file_object, self.log_writer)
            # Check for any missing values
            is_null_present = preprocessor.is_null_present(data)
            if is_null_present:
                data = preprocessor.impute_missing_values(data)

            # If the standard deviation of a column is 0, it means that column has constant values  - drop such columns
            cols_to_drop = preprocessor.get_columns_with_zero_std_deviation(data)
            data = preprocessor.remove_columns(data, cols_to_drop)

            file_loader = file_methods.File_Operation(self.file_object, self.log_writer)
            # Clustering
            kmeans = file_loader.load_model('KMeans')
            # drops the first column for cluster prediction
            clusters = kmeans.predict(data.drop(['Wafer'], axis=1))
            data['clusters'] = clusters
            clusters = data['clusters'].unique()
            for i in clusters:
                cluster_data = data[data['clusters']==i]
                wafer_names = list(cluster_data['Wafer'])
                cluster_data = data.drop(labels=['Wafer'],axis=1)
                cluster_data = cluster_data.drop(['clusters'],axis=1)
                model_name = file_loader.find_correct_model_file(i)
                model = file_loader.load_model(model_name)
                result = list(model.predict(cluster_data))
                result = pd.DataFrame(list(zip(wafer_names,result)),columns=['Wafer','Prediction'])
                path = "Prediction_Output_File/Predictions.csv"
                result.to_csv("Prediction_Output_File/Predictions.csv",header=True,mode='a+')

            self.log_writer.log(self.file_object, 'End of Prediction')

        except Exception as ex:
            self.log_writer.log(self.file_object, 'Error occured while running the prediction!! Error:: %s' % ex)
            raise ex

        return path, result.head().to_json(orient="records")
