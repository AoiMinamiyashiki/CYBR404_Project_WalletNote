from WalletNote_ver_04.Backend.Database.ConnectDatabase import ConnectDatabase

class CreateDatabase(ConnectDatabase):
    def create_tables(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50),
            email VARCHAR(100),
            password VARCHAR(255)
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS records (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            date DATE,
            amount FLOAT,
            category VARCHAR(50),
            type VARCHAR(10)
        )
        """)
        self.conn.commit()
