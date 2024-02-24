import mysql.connector

class UseDatabase:
    """a context manager class that hooks into the with statement
    this class is created to facilitate code reuse throughout the project webapp
    """

    def __init__(self,dbconfig:dict)->None:
        self.dbconfig = dbconfig
        
    def __enter__(self) -> 'cursor':
        self.connection = mysql.connector.connect(**self.dbconfig)
        self.cursor = self.connection.cursor()
        return self.cursor
  
    def __exit__(self,exec_type,exec_value,exec_trace)->None:
        self.connection.commit()
        self.connection.close()
        self.cursor.close()
