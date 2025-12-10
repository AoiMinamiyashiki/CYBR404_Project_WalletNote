from dataclasses import dataclass
from datetime import datetime, date


@dataclass
class InputInformation:
    """
    1件分の入力データを表すクラス
    """

    user_id: int
    date: date
    price: float
    item: str

    @classmethod
    def from_strings(
        cls,
        user_id: int,
        date_str: str,
        price_str: str,
        item: str,
        date_format: str = "%Y-%m-%d",
    ) -> "InputInformation":
        dt = datetime.strptime(date_str, date_format).date()
        price = float(price_str)
        return cls(user_id=user_id, date=dt, price=price, item=item)
