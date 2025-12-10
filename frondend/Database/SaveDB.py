from mysql.connector import Error

from ConnectDB import ConnectDB
from InputInformation import InputInformation


class SaveDB:
    """
    入力されたレコードを MySQL に保存するクラス
    """

    def __init__(self, connector: ConnectDB) -> None:
        self.connector = connector

    def save_record(self, info: InputInformation) -> bool:
        """
        1件のレコードを保存する。成功 True / 失敗 False。
        """
        try:
            conn = self.connector.get_connection()
            cursor = conn.cursor()

            sql = """
                INSERT INTO records (user_id, date, price, item)
                VALUES (%s, %s, %s, %s)
            """
            params = (info.user_id, info.date, info.price, info.item)

            cursor.execute(sql, params)
            conn.commit()
            return True
        except Error as e:
            print(f"[SaveDB] save_record error: {e}")
            return False
        finally:
            try:
                cursor.close()
                conn.close()
            except Exception:
                pass
