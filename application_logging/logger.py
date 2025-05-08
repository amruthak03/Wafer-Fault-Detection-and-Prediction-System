from datetime import datetime

class App_Logger:
    """
    This class is designed to write log messages to a file.
    """
    def __init__(self):
        pass

    def log(self, file_object, log_message):
        """ The log method takes two arguments:
            file_object: A file object where the log messages will be written
            log_message: The actual log message to write
        """
        self.now = datetime.now()  # Fetches the current date and time
        self.date = self.now.data()  # Extracts just the date
        self.current_time = self.now.strftime("%H:%M:%S")  # Formats the current time
        file_object.write(str(self.data) + "/" + str(self.current_time) + "\t\t" + log_message + "\n")  # Combines the
        # date, time, and log message to string format as YYYY-MM-DD/HH:MM:SS log_message and write it to the file
        # object


