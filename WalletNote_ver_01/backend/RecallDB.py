from ConnectDB import ConnectDB


class RecallDB(ConnectDB):
    """
    Retrieve data from database.
    """

    def fetch_all(self):
        conn = self.connect()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM records")
        data = cursor.fetchall()

        self.close()
        return data
