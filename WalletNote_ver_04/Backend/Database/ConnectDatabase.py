import mysql.connector

class ConnectDatabase:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root1234",
            database="walletnote"
        )
        self.cursor = self.conn.cursor(dictionary=True)
