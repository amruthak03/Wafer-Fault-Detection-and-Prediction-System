import pickle
import os
import shutil

class File_Operation:
    """
    This class provides methods to save, load, and manage machine learning models. It is designed for use in a machine
    learning pipeline, ensuring that models are stored securely and can be retrieved when needed, with robust logging
    and error handling for debugging.
    """

    def __init__(self, file_object, logger_object):
        self.file_object = file_object
        self.logger_object = logger_object
        self.model_directory = 'models/'

    def save_model(self, model, filename):
        """
        This method saves a trained model as a serialized file using Python's pickle module.
        Steps:
            Constructs a directory path for the model using self.model_directory and filename.
            If a directory for the model already exists, deletes the existing directory using shutil.rmtree.
            Creates a new directory and saves the model using pickle.dump
            Logs success or raises an exception if any errors occur.
        Returns: 'success' if the model is saved successfully.
        """

        self.logger_object.log(self.file_object, 'Entered the save_model method of the File_Operation class')
        try:
            # create separate directory for each cluster
            path = os.path.join(self.model_directory, filename)
            # remove previously existing models for each clusters
            if os.path.isdir(path):
                shutil.rmtree(self.model_directory)
                os.makedirs(path)
            else:
                os.makedirs(path)
            with open(path + '/' + filename + '.sav', 'wb') as f:
                # save the model
                pickle.dump(model, f)
            self.logger_object.log(self.file_object, 'Model file' + filename +
                                   'saved. Exited the save_model method of the Model_Finder class')
            return 'success'
        except Exception as e:
            self.logger_object.log(self.file_object,
                                   'Exception occured in save_model method of the Model_Finder class. Exception message:'
                                   + str(e))
            self.logger_object.log(self.file_object, 'Model File' + filename +
                                   'could not be saved. Exited the save_model method of the Model_Finder class')
            raise Exception()

    def load_model(self, filename):
        """
        This method loads a saved model file into memory.
        Steps:
            Constructs the path to the model file (filename.sav) in the appropriate subdirectory.
            Loads the model using pickle.load.
            Logs success or raises an exception if any errors occur.
        Returns: The loaded model object.
        """
        self.logger_object.log(self.file_object, 'Entered the load_model method of the File_Operation class')
        try:
            with open(self.model_directory + filename + '/' + filename + '.sav','rb') as f:
                self.logger_object.log(self.file_object, 'Model File ' + filename +
                                       ' loaded. Exited the load_model method of the Model_Finder class')
                return pickle.load(f)
        except Exception as e:
            self.logger_object.log(self.file_object,
                                   'Exception occured in load_model method of the Model_Finder class. Exception message:'
                                   + str(e))
            self.logger_object.log(self.file_object, 'Model File ' + filename +
                                   ' could not be saved. Exited the load_model method of the Model_Finder class')
            raise Exception()

    def find_correct_model_file(self,cluster_number):
        """
        This method identifies the correct model file based on a given cluster number.
        Steps:
            Lists all files in self.model_directory.
            Iterates through the files and checks if the cluster number is part of the filename.
            Extracts and returns the model filename (without the extension) if it matches.
        Returns: The model filename corresponding to the cluster number.
        """
        self.logger_object.log(self.file_object,
                               'Entered the find_correct_model_file method of the File_Operation class')
        try:
            self.cluster_number = cluster_number
            self.folder_name = self.model_directory
            self.list_of_model_files = []
            self.list_of_files = os.listdir(self.folder_name)
            for self.file in self.list_of_files:
                try:
                    if self.file.index(str(self.cluster_number)) != -1:
                        self.model_name = self.file
                except:
                    continue
            self.model_name = self.model_name.split('.')[0]
            self.logger_object.log(self.file_object,
                                           'Exited the find_correct_model_file method of the Model_Finder class.')
            return self.model_name
        except Exception as e:
            self.logger_object.log(self.file_object,
                                   'Exception occured in find_correct_model_file method of the Model_Finder class. '
                                   'Exception message:  ' + str(e))
            self.logger_object.log(self.file_object,
                                   'Exited the find_correct_model_file method of the Model_Finder class with Failure')
            raise Exception()

