from sklearn.model_selection import train_test_split
from data_ingestion import data_loader
from data_preprocessing import preprocessing
from data_preprocessing import clustering
from best_model_finder import tuner
from file_operations import file_methods
from application_logging import logger

class trainModel:
    """
    This script represents the entry point for training a machine learning model using a structured pipeline. It
    encompasses data ingestion, preprocessing, clustering, model selection, and saving the trained models for later use.
    This class orchestrates these steps while logging the progress and handling exceptions.
    """

    def __init__(self):
        self.log_writer = logger.App_Logger()
        self.file_object = open("Training_Logs/ModelTrainingLog.txt", 'a+')

    def trainingModel(self):
        """
        This method implements the entire model training pipeline.
        Steps:
            Logs the start of the training process.
            Fetches the raw dataset for training.
            Performs various data cleaning and preparation steps.
            Groups data into clusters to build separate models for each cluster.
            For each cluster, model selection, training, and saves the model.
            Error Handling
        """
        self.log_writer.log(self.file_object, 'Start of training.')
        try:
            # Getting the data from the source
            data_getter = data_loader.Data_Getter(self.file_object, self.log_writer)
            data = data_getter.get_data()

            # Data Preprocessing
            preprocessor = preprocessing.Preprocessor(self.file_object, self.log_writer)
            # remove the unnamed column as it doesn't contribute to prediction.
            data = preprocessor.remove_columns(data, ['Wafer'])
            # Create separate features and labels
            X, Y = preprocessor.separate_label_features(data, label_column_name='Output')
            # Check for any missing values
            is_null_present = preprocessor.is_null_present(X)
            # If missing values are present, impute
            if is_null_present:
                X = preprocessor.impute_missing_values(X)

            # If the standard deviation of a column is 0, it means that column has constant values  - drop such columns
            cols_to_drop = preprocessor.get_columns_with_zero_std_deviation(X)
            X = preprocessor.remove_columns(X, cols_to_drop)

            # Applying Clustering approach
            kmeans = clustering.KMeansClustering(self.file_object, self.log_writer)
            # using the elbow plot to find the number of optimum clusters
            number_of_clusters = kmeans.elbow_plot(X)
            # Divide the data into clusters
            X = kmeans.create_clusters(X, number_of_clusters)
            # create a new column in the dataset consisting of the corresponding cluster assignments
            X['Labels'] = Y
            # Getting unique clusters from our data
            list_of_clusters = X['Cluster'].unique()

            # Parsing all the clusters and looking for the best ML algorithm to fit on individual cluster
            for i in list_of_clusters:
                cluster_data = X[X['Cluster']==i] # filters the data for one cluster
                # Prepare the feature and Label columns
                cluster_features = cluster_data.drop(['Labels','Cluster'], axis=1)
                cluster_label = cluster_data['Labels']

                # Splitting the data into train and test sets for each cluster
                x_train, x_test, y_train, y_test = train_test_split(cluster_features, cluster_label, test_size=1 / 3,
                                                                    random_state=355)
                model_finder = tuner.Model_Finder(self.file_object, self.log_writer)
                # Getting the best model for each cluster
                best_model_name, best_model = model_finder.get_best_model(x_train, y_train, x_test, y_test)
                # Saving the best model
                file_op = file_methods.File_Operation(self.file_object, self.log_writer)
                save_model = file_op.save_model(best_model, best_model_name + str(i))

            # Logging the success of Training
            self.log_writer.log(self.file_object, 'Successful End of Training.')
            self.file_object.close()

        except Exception:
            self.log_writer.log(self.file_object, 'Unsuccessful End of Training')
            self.file_object.close()
            raise Exception