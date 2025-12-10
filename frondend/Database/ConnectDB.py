import mysql.connector
from mysql.connector import Error


class ConnectDB:
    """
    MySQLへの接続だけを担当するクラス
    必要に応じて host / user / password / database を書き換えて使う
    """

    def __init__(
        self,
        host: str = "localhost",
        user: str = "root",
        password: str = "password",
        database: str = "walletnote",
    ) -> None:
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def get_connection(self, use_database: bool = True):
        """
        MySQLコネクションを返す。
        use_database=False の場合は database を指定せずに接続（DB作成用）。
        """
        try:
            if use_database:
                conn = mysql.connector.connect(
                    host=self.host,
                    user=self.user,
                    password=self.password,
                    database=self.database,
                )
            else:
                conn = mysql.connector.connect(
                    host=self.host,
                    user=self.user,
                    password=self.password,
                )
            return conn
        except Error as e:
            print(f"[ConnectDB] Connection error: {e}")
            raise
