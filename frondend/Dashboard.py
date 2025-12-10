from typing import Optional
from datetime import date

import pandas as pd

from RecallDB import RecallDB
from MakeGraph import MakeGraph


class Dashboard:
    """
    InputInformation / RecallDB から受け取ったデータを
    表やグラフにまとめるクラス
    """

    def __init__(self, recall_db: RecallDB) -> None:
        self.recall_db = recall_db
        self._graph = MakeGraph()

    def get_dataframe(
        self,
        user_id: int,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ) -> pd.DataFrame:
        """
        指定ユーザーの記録を DataFrame で取得
        """
        return self.recall_db.fetch_records_df(user_id, start_date, end_date)

    def show_pie_chart(
        self,
        user_id: int,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        save_path: Optional[str] = None,
    ) -> None:
        """
        item別の支出割合パイチャート
        """
        df = self.get_dataframe(user_id, start_date, end_date)
        self._graph.pie_by_item(df, save_path=save_path)

    def show_bar_chart(
        self,
        user_id: int,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        save_path: Optional[str] = None,
    ) -> None:
        """
        日付別の合計支出棒グラフ
        """
        df = self.get_dataframe(user_id, start_date, end_date)
        self._graph.bar_by_date(df, save_path=save_path)

    def show_all(
        self,
        user_id: int,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ) -> None:
        """
        パイチャート + 棒グラフをまとめて表示
        """
        df = self.get_dataframe(user_id, start_date, end_date)
        self._graph.pie_by_item(df)
        self._graph.bar_by_date(df)
