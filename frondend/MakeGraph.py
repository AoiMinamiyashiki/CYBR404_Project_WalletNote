from typing import Optional

import matplotlib.pyplot as plt
import pandas as pd


class MakeGraph:
    """
    グラフ描画専用のクラス
    Dashboard から呼び出される想定
    """

    def __init__(self) -> None:
        # 必要ならスタイル設定など
        pass

    def pie_by_item(self, df: pd.DataFrame, title: str = "Spending by Item", save_path: Optional[str] = None) -> None:
        """
        item 別の支出割合をパイチャートで表示
        """
        if df.empty:
            print("[MakeGraph] DataFrame is empty (pie chart skipped).")
            return

        grouped = df.groupby("item")["price"].sum()

        plt.figure()
        grouped.plot(kind="pie", autopct="%1.1f%%")
        plt.title(title)
        plt.ylabel("")

        if save_path:
            plt.savefig(save_path, bbox_inches="tight")
        else:
            plt.show()

        plt.close()

    def bar_by_date(self, df: pd.DataFrame, title: str = "Spending by Date", save_path: Optional[str] = None) -> None:
        """
        date 別の合計支出を棒グラフで表示
        """
        if df.empty:
            print("[MakeGraph] DataFrame is empty (bar chart skipped).")
            return

        grouped = df.groupby("date")["price"].sum()

        plt.figure()
        grouped.plot(kind="bar")
        plt.title(title)
        plt.xlabel("Date")
        plt.ylabel("Total Price")

        plt.xticks(rotation=45, ha="right")

        plt.tight_layout()
        if save_path:
            plt.savefig(save_path, bbox_inches="tight")
        else:
            plt.show()

        plt.close()
