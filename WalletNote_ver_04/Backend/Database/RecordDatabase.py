from WalletNote_ver_04.Backend.Database.ConnectDatabase import ConnectDatabase

class RecordDatabase(ConnectDatabase):
    def save(self, user_id, date, amount, category, type_):
        self.cursor.execute(
            """
            INSERT INTO records (user_id, date, amount, category, type)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (user_id, date, amount, category, type_)
        )
        self.conn.commit()
