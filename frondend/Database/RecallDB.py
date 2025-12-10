from typing import List, Dict, Optional
from datetime import date
from mysql.connector import Error

import pandas as pd

from ConnectDB import ConnectDB


class RecallDB:
    """
    MySQLから記録を呼び出すクラス
    """

    def __init__(self, connector: ConnectDB) -> None:
        self.connector = connector

    def fetch_records(
        self,
        user_id: int,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ) -> List[Dict]:
        """
        指定ユーザーのレコード一覧を dict のリストで返す。
        日付範囲はオプション。
        """
        try:
            conn = self.connector.get_connection()
            cursor = conn.cursor(dictionary=True)

            base_sql = """
                SELECT id, user_id, date, price, item, created_at
                FROM records
                WHERE user_id = %s
            """
            params = [user_id]

            if start_date:
                base_sql += " AND date >= %s"
                params.append(start_date)
            if end_date:
                base_sql += " AND date <= %s"
                params.append(end_date)

            base_sql += " ORDER BY date ASC, id ASC"

            cursor.execute(base_sql, tuple(params))
            rows = cursor.fetchall()
            return rows
        except Error as e:
            print(f"[RecallDB] fetch_records error: {e}")
            return []
        finally:
            try:
                cursor.close()
                conn.close()
            except Exception:
                pass

    def fetch_records_df(
        self,
        user_id: int,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ) -> pd.DataFrame:
        """
        pandas.DataFrame でレコードを返す。
        Dashboard からそのまま使える想定。
        """
        records = self.fetch_records(user_id, start_date, end_date)
        if not records:
            return pd.DataFrame(columns=["id", "user_id", "date", "price", "item", "created_at"])
        df = pd.DataFrame(records)
        # 日付を Date 型にしておく
        if "date" in df.columns:
            df["date"] = pd.to_datetime(df["date"]).dt.date
        return df
