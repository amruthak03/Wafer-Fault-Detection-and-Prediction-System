import shutil
import sqlite3
from datetime import datetime
from os import listdir
import os
import csv
from application_logging.logger import App_Logger


class dBOperation:
    """
    This class handles database-related operations for managing prediction data. The operations include creating and
    connecting to a SQLite database, creating a table, inserting data into the table, and exporting data from the
    database to a CSV file.
    """

    def __init__(self):
        self.path = 'Prediction_Database/'
        self.badFilePath = "Prediction_Raw_Files_Validated/Bad_Raw"
        self.goodFilePath = "Prediction_Raw_Files_Validated/Good_Raw"
        self.logger = App_Logger()

    def dataBaseConnection(self, DatabaseName):
        """
        This method establishes a connection to the SQLite database. If the database doesn't exist, it creates one.
        Also, logs success or failure to a log file.
        :parameter: DatabaseName: Name of the database to connect to or create
        :returns Connection object (conn).
        """
        try:
            conn = sqlite3.connect(self.path + DatabaseName + '.db')
            file = open("Prediction_Logs/DataBaseConnectionLog.txt", 'a+')
            self.logger.log(file, "Opened %s database successfully" % DatabaseName)
            file.close()

        except ConnectionError:
            file = open("Prediction_Logs/DataBaseConnectionLog.txt", 'a+')
            self.logger.log(file, "Error while connecting to database: %s" % ConnectionError)
            file.close()
            raise ConnectionError

        return conn

    def createTableDb(self, DatabaseName, column_names):
        """
        This method creates a table named Good_Raw_Data in the specified database. Drops the table if it already exists.
        Iterates over column_names (dictionary of column names and data types) to create or alter the table structure.
        Logs success or failure to DbTableCreateLog.txt.
        :param DatabaseName: The name of the database
        :param column_names: A dictionary where keys are column names and values are data types.
        """
        try:
            conn = self.dataBaseConnection(DatabaseName)
            conn.execute('DROP THE TABLE Good_Raw_Data IF EXISTS;')
            for key in column_names.keys():
                type = column_names[key]
                try:
                    conn.execute(
                        'ALTER TABLE Good_Raw_Data ADD COLUMN "{column_name}" {dataType}'.format(column_name=key,
                                                                                                 dataType=type))
                except:
                    conn.execute(
                        'CREATE TABLE Good_Raw_Data ({column_name} {dataType})'.format(column_name=key, dataType=type))
            conn.close()
            file = open("Prediction_Logs/DbTableCreateLog.txt", 'a+')
            self.logger.log(file, "Tables created successfully!!")
            file.close()

            file = open("Prediction_Logs/DataBaseConnectionLog.txt", 'a+')
            self.logger.log(file, "Closed %s database successfully" % DatabaseName)
            file.close()

        except Exception as e:
            file = open("Prediction_Logs/DbTableCreateLog.txt", 'a+')
            self.logger.log(file, "Error while creating table: %s " % e)
            file.close()
            conn.close()
            file = open("Prediction_Logs/DataBaseConnectionLog.txt", 'a+')
            self.logger.log(file, "Closed %s database successfully" % DatabaseName)
            file.close()
            raise e

    def insertIntoTableGoodData(self, Database):
        """
        This method reads data from files in the Good_Raw directory and inserts the records into the Good_Raw_Data table.
        Moves files causing errors to the Bad_Raw directory. Logs the process in DbInsertLog.txt.
        :param Database: Name of the database to insert data into.
        :return: None
        """
        conn = self.dataBaseConnection(Database)
        goodFilePath = self.goodFilePath
        badFilePath = self.badFilePath
        onlyfiles = [f for f in listdir(goodFilePath)]
        log_file = open("Prediction_Logs/DbInsertLog.txt", 'a+')
        for file in onlyfiles:
            try:
                with open(goodFilePath + '/' + file, "r") as f:
                    next(f)
                    reader = csv.reader(f, delimiter="\n")
                    for line in enumerate(reader):
                        for list_ in line[1]:
                            try:
                                conn.execute('INSERT INTO Good_Raw_Data values ({values})'.format(values=(list_)))
                                self.logger.log(log_file, " %s: File loaded successfully!!" % file)
                                conn.commit()
                            except Exception as e:
                                raise e
            except Exception as e:
                conn.rollback()
                self.logger.log(log_file, "Error while creating table: %s " % e)
                shutil.move(goodFilePath + '/' + file, badFilePath)
                self.logger.log(log_file, "File Moved Successfully %s" % file)
                log_file.close()
                conn.close()
                raise e
        conn.close()
        log_file.close()

    def selectingDatafromtableintocsv(self, Database):
        """
        This method exports all data from the Good_Raw_Data table into a CSV file. Logs success or failure to
        ExportToCsv.txt.
        :param Database: Name of the database to export data from.
        :return: None
        """
        self.fileFromDb = 'Prediction_FileFromDB/'
        self.fileName = 'InputFile.csv'
        log_file = open("Prediction_Logs/ExportToCsv.txt", 'a+')
        try:
            conn = self.dataBaseConnection(Database)
            sqlSelect = "SELECT *  FROM Good_Raw_Data"
            cursor = conn.cursor()
            cursor.execute(sqlSelect)
            results = cursor.fetchall()
            # Get the headers of the csv file
            headers = [i[0] for i in cursor.description]
            # Make the CSV output directory
            if not os.path.isdir(self.fileFromDb):
                os.makedirs(self.fileFromDb)
            # Open CSV file for writing
            csvFile = csv.writer(open(self.fileFromDb + self.fileName, 'w', newline=''), delimiter=',',
                                 lineterminator='\r\n', quoting=csv.QUOTE_ALL, escapechar='\\')
            # Add the header and data to the CSV file
            csvFile.writerow(headers)
            csvFile.writerows(results)
            self.logger.log(log_file, "File exported successfully!!!")
        except Exception as e:
            self.logger.log(log_file, "File exporting failed. Error : %s" % e)
            raise e
