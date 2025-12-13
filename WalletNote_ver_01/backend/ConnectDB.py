import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG


class ConnectDB:
    """
    Base class for MySQL connection.
    """

    def __init__(self):
        self.connection = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=DB_CONFIG["host"],
                user=DB_CONFIG["user"],
                password=DB_CONFIG["password"],
                database=DB_CONFIG["database"]
            )
            return self.connection
        except Error as e:
            print(f"[DB ERROR] {e}")
            return None

    def close(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
