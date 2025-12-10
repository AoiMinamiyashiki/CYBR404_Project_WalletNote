from mysql.connector import Error
from ConnectDB import ConnectDB


class AddDB:
    """
    データベースとテーブルを作成するクラス
    """

    def __init__(self, connector: ConnectDB) -> None:
        self.connector = connector

    def create_database(self) -> None:
        """
        walletnote データベースを作成
        """
        try:
            conn = self.connector.get_connection(use_database=False)
            cursor = conn.cursor()
            cursor.execute(
                f"CREATE DATABASE IF NOT EXISTS {self.connector.database} "
                "DEFAULT CHARACTER SET 'utf8mb4'"
            )
            conn.commit()
        except Error as e:
            print(f"[AddDB] create_database error: {e}")
            raise
        finally:
            try:
                cursor.close()
                conn.close()
            except Exception:
                pass

    def create_tables(self) -> None:
        """
        users テーブル / records テーブルを作成
        """
        try:
            conn = self.connector.get_connection(use_database=True)
            cursor = conn.cursor()

            create_users = """
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) NOT NULL UNIQUE,
                password_hash VARCHAR(255) NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """

            create_records = """
            CREATE TABLE IF NOT EXISTS records (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                date DATE NOT NULL,
                price DECIMAL(10, 2) NOT NULL,
                item VARCHAR(255) NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                CONSTRAINT fk_records_user
                    FOREIGN KEY (user_id) REFERENCES users (id)
                    ON DELETE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """

            cursor.execute(create_users)
            cursor.execute(create_records)
            conn.commit()
        except Error as e:
            print(f"[AddDB] create_tables error: {e}")
            raise
        finally:
            try:
                cursor.close()
                conn.close()
            except Exception:
                pass

    def setup_all(self) -> None:
        """
        DB + テーブルをまとめてセットアップ
        """
        self.create_database()
        self.create_tables()
