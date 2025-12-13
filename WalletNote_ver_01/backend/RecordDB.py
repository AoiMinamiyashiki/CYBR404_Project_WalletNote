from ConnectDB import ConnectDB


class RecordDB(ConnectDB):
    """
    Insert data into records table.
    """

    def insert(self, input_info):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO records (price, date, service) VALUES (%s, %s, %s)",
            (input_info.price, input_info.date, input_info.service_or_product)
        )

        conn.commit()
        self.close()
