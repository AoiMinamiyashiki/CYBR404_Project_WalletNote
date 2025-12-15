from WalletNote_ver_04.Backend.Database.ConnectDatabase import ConnectDatabase

class RecallDatabase(ConnectDatabase):
    def fetch_by_user(self, user_id):
        self.cursor.execute(
            "SELECT * FROM records WHERE user_id=%s ORDER BY date DESC",
            (user_id,)
        )
        return self.cursor.fetchall()
