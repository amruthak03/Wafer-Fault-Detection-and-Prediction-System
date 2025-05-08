import shutil
import sqlite3
from datetime import datetime
from os import listdir
import os
import csv
from application_logging.logger import App_Logger


class dBOperation:
    """
     This class is used to handle all the DB operations in the training phase
    """

    def __init__(self):
        self.path = 'Training_Database/'
        self.badFilePath = "Training_Raw_files_validated/Bad_Raw"
        self.goodFilePath = "Training_Raw_files_validated/Good_Raw"
        self.logger = App_Logger()

    def dataBaseConnection(self, DatabaseName):
        """
        This method creates a database with the given name and if that DB already exists then it opens the connection to
        that DB.
        :param DatabaseName: Name of the database
        :return: Connection the database
        """
        try:
            conn = sqlite3.connect(self.path + DatabaseName + '.db')
            file = open("Training_logs/DatabaseConnectionLog.txt", 'a+')
            self.logger.log(file, "Opened as %s database successfully" % DatabaseName)
            file.close()

        except ConnectionError:
            file = open("Training_Logs/DataBaseConnectionLog.txt", 'a+')
            self.logger.log(file, "Error while connecting to database: %s" % ConnectionError)
            file.close()
            raise ConnectionError

        return conn

    def createTableDb(self, DatabaseName, column_names):
        """
        This method creates a table in the given database which will be used to insert the Good data after raw data
        validation.
        :param DatabaseName: Name of the database
        :param column_names: A dictionary where keys are column names and values are data types.
        :return: None
        """
        try:
            conn = self.dataBaseConnection(DatabaseName)
            c = conn.cursor()
            c.execute("SELECT count(name)  FROM sqlite_master WHERE type = 'table'AND name = 'Good_Raw_Data'")
            if c.fetchone()[0] == 1:
                conn.close()
                file = open("Training_Logs/DbTableCreateLog.txt", 'a+')
                self.logger.log(file, "Tables created successfully!!")
                file.close()

                file = open("Training_Logs/DataBaseConnectionLog.txt", 'a+')
                self.logger.log(file, "Closed %s database successfully" % DatabaseName)
                file.close()

            else:
                for key in column_names.keys():
                    type = column_names[key]
                    try:
                        conn.execute(
                            'ALTER TABLE Good_Raw_Data ADD COLUMN "{column_name}" {dataType}'.format(column_name=key,
                                                                                                     dataType=type))
                    except:
                        conn.execute('CREATE TABLE  Good_Raw_Data ({column_name} {dataType})'.format(column_name=key,
                                                                                                     dataType=type))
                conn.close()

                file = open("Training_Logs/DbTableCreateLog.txt", 'a+')
                self.logger.log(file, "Tables created successfully!!")
                file.close()

                file = open("Training_Logs/DataBaseConnectionLog.txt", 'a+')
                self.logger.log(file, "Closed %s database successfully" % DatabaseName)
                file.close()

        except Exception as e:
            file = open("Training_Logs/DbTableCreateLog.txt", 'a+')
            self.logger.log(file, "Error while creating table: %s " % e)
            file.close()
            conn.close()
            file = open("Training_Logs/DataBaseConnectionLog.txt", 'a+')
            self.logger.log(file, "Closed %s database successfully" % DatabaseName)
            file.close()
            raise e

    def insertIntoTableGoodData(self, Database):
        """
        This method inserts the Good data files from the Good_Raw folder into the
        above created table.
        :param Database: Database name
        :return: None
        """

        conn = self.dataBaseConnection(Database)
        goodFilePath = self.goodFilePath
        badFilePath = self.badFilePath
        onlyfiles = [f for f in listdir(goodFilePath)]
        log_file = open("Training_Logs/DbInsertLog.txt", 'a+')
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

        conn.close()
        log_file.close()

    def selectingDatafromtableintocsv(self, Database):
        """
        This method exports the data into the GoodData table as a CSV file.
        :param Database: name of the database
        :return: None
        """
        self.fileFromDb = 'Training_FileFromDB/'
        self.fileName = 'InputFile.csv'
        log_file = open("Training_Logs/ExportToCsv.txt", 'a+')
        try:
            conn = self.dataBaseConnection(Database)
            sqlSelect = "SELECT *  FROM Good_Raw_Data"
            cursor = conn.cursor()
            cursor.execute(sqlSelect)
            results = cursor.fetchall()
            # Get the headers of the csv file
            headers = [i[0] for i in cursor.description]
            if not os.path.isdir(self.fileFromDb):
                os.makedirs(self.fileFromDb)

            csvFile = csv.writer(open(self.fileFromDb + self.fileName, 'w', newline=''), delimiter=',',
                                 lineterminator='\r\n', quoting=csv.QUOTE_ALL, escapechar='\\')
            csvFile.writerow(headers)
            csvFile.writerows(results)
            self.logger.log(log_file, "File exported successfully!!!")
            log_file.close()

        except Exception as e:
            self.logger.log(log_file, "File exporting failed. Error : %s" % e)
            log_file.close()
