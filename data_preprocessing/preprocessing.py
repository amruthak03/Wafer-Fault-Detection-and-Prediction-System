import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer

class Preprocessor:
    """
    This class is designed to handle various preprocessing tasks for cleaning and transforming data before training a
    machine learning model. It incorporates robust logging and error handling, making it easier to identify and address
    issues in the preprocessing pipeline.
    """

    def __init__(self, file_object, logger_object):
        self.file_object = file_object
        self.logger_object = logger_object

    def remove_columns(self, data, columns):
        """
        Removes specified columns from a DataFrame
        Steps:
            Logs entry into the method.
            Uses pandas.DataFrame.drop to remove columns specified in the columns list.
            Logs success or exception.
        Returns: A new DataFrame with specified columns removed.
        """
        self.logger_object.log(self.file_object, 'Entered the remove_columns method of the Preprocessor class')
        self.data = data
        self.columns = columns
        try:
            # drop the labels specified in the columns
            self.useful_data = self.data.drop(labels=self.columns, axis=1)
            self.logger_object.log(self.file_object,
                                   'Column removal Successful. Exited the remove_columns method of the Preprocessor class')
            return self.useful_data
        except Exception as e:
            self.logger_object.log(self.file_object,
                                   'Exception occurred in remove_columns method of the Preprocessor class. Exception message:'
                                   + str(e))
            self.logger_object.log(self.file_object,
                                   'Column removal Unsuccessful. Exited the remove_columns method of the Preprocessor class')
            raise Exception()

    def separate_label_features(self, data, label_column_name):
        """
        This splits the DataFrame into features (X) and labels (Y).
        Steps:
            Logs entry into the method.
            Separate features by dropping the label column using drop.
            Extracts the label column as Y.
            Logs success or exception.
        Returns: Two DataFrames - one for features and one for the label.
        """
        self.logger_object.log(self.file_object, 'Entered the separate_label_feature method of the Preprocessor class')
        try:
            # drop the columns specified and separate the feature columns
            self.X = data.drop(labels=label_column_name, axis=1)
            self.Y = data[label_column_name] # Filter the Label columns
            self.logger_object.log(self.file_object,
                                   'Label Separation Successful. Exited the separate_label_feature method of the Preprocessor class')
            return self.X, self.Y
        except Exception as e:
            self.logger_object.log(self.file_object,
                                   'Exception occured in separate_label_feature method of the Preprocessor class. Exception message:'
                                   + str(e))
            self.logger_object.log(self.file_object,
                                   'Label Separation Unsuccessful. Exited the separate_label_feature method of the Preprocessor class')
            raise Exception()

    def is_null_present(self, data):
        """
        This method checks if the DataFrame contains any null (missing) values.
        Steps:
            Logs entry into the method.
            Uses pandas.DataFrame.isna().sum() to count missing values per column.
            If any null values are found, logs and saves a CSV file (null_values.csv) with details of columns and their missing value counts.
            Logs success or exception.
        Returns: A boolean indicating if null values are present.
        """
        self.logger_object.log(self.file_object, 'Entered the is_null_present method of the Preprocessor class')
        self.null_present = False
        try:
            # check for the count of null values per column
            self.null_counts = data.isna().sum()
            for i in self.null_counts:
                if i > 0:
                    self.null_present = True
                    break
            if self.null_present:
                dataframe_with_null = pd.DataFrame()
                dataframe_with_null['columns'] = data.columns
                dataframe_with_null['missing values count'] = np.asarray(data.isna().sum())
                # storing the null column information to file
                dataframe_with_null.to_csv('preprocessing_data/null_values.csv')
            self.logger_object.log(self.file_object,
                                   'Finding missing values is a success.'
                                   'Data written to the null values file. Exited the is_null_present method of the Preprocessor class')
            return self.null_present
        except Exception as e:
            self.logger_object.log(self.file_object,
                                   'Exception occured in is_null_present method of the Preprocessor class. Exception message:'
                                   + str(e))
            self.logger_object.log(self.file_object,
                                   'Finding missing values failed. Exited the is_null_present method of the Preprocessor class')
            raise Exception()

    def impute_missing_values(self, data):
        """
        This method fills missing values using the K-Nearest Neighbors (KNN) Imputation technique.
        Steps:
            Logs entry into the method.
            Creates a KNNImputer instance with n_neighbors=3.
            Fits the imputer to the data and transforms it.
            Converts the resulting numpy array back to a DataFrame with the original column names.
            Logs success or exception.
        Returns: A DataFrame with missing values imputed.
        """
        self.logger_object.log(self.file_object, 'Entered the impute_missing_values method of the Preprocessor class')
        self.data = data
        try:
            imputer = KNNImputer(n_neighbors=3, weights='uniform', missing_values=np.nan)
            # impute the missing values
            self.new_array = imputer.fit_transform(self.data)
            # convert the nd-array to a DataFrame
            self.new_data = pd.DataFrame(data=self.new_array, columns=self.data.columns)
            self.logger_object.log(self.file_object,
                                   'Imputing missing values Successful. Exited the impute_missing_values method of the Preprocessor class')
            return self.new_data
        except Exception as e:
            self.logger_object.log(self.file_object,
                                   'Exception occured in impute_missing_values method of the Preprocessor class. Exception message:'
                                   + str(e))
            self.logger_object.log(self.file_object,
                                   'Imputing missing values failed. Exited the impute_missing_values method of the Preprocessor class')
            raise Exception()

    def get_columns_with_zero_std_deviation(self, data):
        """
        This method identifies columns with zero standard deviation (constant values).
        Steps:
            Logs entry into the method.
            Computes statistical summary of the data using data.describe().
            Iterates through columns, checking for a standard deviation (std) of zero.
            Logs success or exception.
        Returns: A list of column names with zero standard deviation.
        """
        self.logger_object.log(self.file_object,
                               'Entered the get_columns_with_zero_std_deviation method of the Preprocessor class')
        self.columns = data.columns
        self.data_n = data.describe()
        self.col_to_drop = []
        try:
            for x in self.columns:
                # check if standard deviation is zero
                if self.data_n[x]['std'] == 0:
                    self.col_to_drop.append(x)
            self.logger_object.log(self.file_object,
                                   'Column search for Standard Deviation of Zero Successful. '
                                   'Exited the get_columns_with_zero_std_deviation method of the Preprocessor class')
            return self.col_to_drop
        except Exception as e:
            self.logger_object.log(self.file_object,
                                   'Exception occured in get_columns_with_zero_std_deviation method of the Preprocessor class. '
                                   'Exception message:  ' + str(e))
            self.logger_object.log(self.file_object,
                                   'Column search for Standard Deviation with Zeros Failed. '
                                   'Exited the get_columns_with_zero_std_deviation method of the Preprocessor class')
            raise Exception()
        

