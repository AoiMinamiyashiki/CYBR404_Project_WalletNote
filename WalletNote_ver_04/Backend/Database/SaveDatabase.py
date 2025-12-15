from WalletNote_ver_04.Backend.Database.ConnectDatabase import ConnectDatabase

class SaveDatabase(ConnectDatabase):
    def save_user(self, username, email, password):
        self.cursor.execute(
            "INSERT INTO users (username, email, password) VALUES (%s,%s,%s)",
            (username, email, password)
        )
        self.conn.commit()
