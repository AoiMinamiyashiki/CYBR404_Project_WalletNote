import hashlib
from typing import Optional
from mysql.connector import Error

from ConnectDB import ConnectDB


class UserInformation:
    """
    ログイン／新規ユーザー登録を扱うクラス
    """

    _SALT = "walletnote_static_salt"  # 必要なら変更

    def __init__(self, connector: ConnectDB) -> None:
        self.connector = connector

    def _hash_password(self, raw_password: str) -> str:
        """
        非推奨だが授業用の簡易ハッシュ（本番はbcryptなどを使うべき）
        """
        text = (self._SALT + raw_password).encode("utf-8")
        return hashlib.sha256(text).hexdigest()

    def register(self, username: str, password: str) -> bool:
        """
        新規ユーザー登録。成功 True / 既に存在 or エラーで False
        """
        try:
            conn = self.connector.get_connection()
            cursor = conn.cursor()

            # 既存チェック
            cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
            if cursor.fetchone():
                return False

            password_hash = self._hash_password(password)

            cursor.execute(
                "INSERT INTO users (username, password_hash) VALUES (%s, %s)",
                (username, password_hash),
            )
            conn.commit()
            return True
        except Error as e:
            print(f"[UserInformation] register error: {e}")
            return False
        finally:
            try:
                cursor.close()
                conn.close()
            except Exception:
                pass

    def authenticate(self, username: str, password: str) -> Optional[int]:
        """
        ログイン認証。成功時は user_id を返す。失敗時は None。
        """
        try:
            conn = self.connector.get_connection()
            cursor = conn.cursor()

            cursor.execute(
                "SELECT id, password_hash FROM users WHERE username = %s",
                (username,),
            )
            row = cursor.fetchone()
            if not row:
                return None

            user_id, password_hash_db = row
            if password_hash_db == self._hash_password(password):
                return user_id
            return None
        except Error as e:
            print(f"[UserInformation] authenticate error: {e}")
            return None
        finally:
            try:
                cursor.close()
                conn.close()
            except Exception:
                pass
