from ConnectDB import ConnectDB


class CreateDB(ConnectDB):
    """
    Create database tables.
    """

    def create_tables(self):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS records (
            id INT AUTO_INCREMENT PRIMARY KEY,
            price FLOAT NOT NULL,
            date DATE NOT NULL,
            service VARCHAR(255) NOT NULL
        )
        """)

        conn.commit()
        self.close()
