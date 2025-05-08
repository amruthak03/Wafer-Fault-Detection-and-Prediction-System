from datetime import datetime
from os import listdir
import pandas as pd
from application_logging.logger import App_Logger


class dataTransformPredict:
    """
    This class focuses on transforming data in files located in the "Good_Raw" directory. It ensures the data is ready
    for further processing or storage in a database. The class primarily deals with replacing missing values and
    modifying specific columns.
    """

    def __init__(self):
        self.goodDataPath = "Prediction_Raw_Files_Validated/Good_Raw"
        self.logger = App_Logger()

    def replaceMissingWithNull(self):
        """
        This method replaces missing values in all files located in the Good_Raw directory with the string "NULL".
        Modifies the Wafer column by keeping only a substring (starting from the 6th character). Saves the
        transformed files back to the same directory.
        :return: None
        """
        try:
            log_file = open("Prediction_Logs/dataTransformLog.txt", 'a+')
            onlyfiles = [f for f in listdir(self.goodDataPath)]
            for file in onlyfiles:
                csv = pd.read_csv(self.goodDataPath + "/" + file)
                csv.fillna('NULL', inplace=True)
                csv['Wafer'] = csv['Wafer'].str[6:]
                csv.to_csv(self.goodDataPath + "/" + file, index=None, header=True)
                self.logger.log(log_file, " %s: File Transformed successfully!!" % file)

        except Exception as e:
            self.logger.log(log_file, "Data Transformation failed because:: %s" % e)
            log_file.close()
            raise e

        log_file.close()
