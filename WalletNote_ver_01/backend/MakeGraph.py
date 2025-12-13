import matplotlib.pyplot as plt
from RecallDB import RecallDB


class MakeGraph:
    """
    Generate graphs from database data.
    """

    def monthly_graph(self):
        data = RecallDB().fetch_all()

        dates = [row["date"] for row in data]
        prices = [row["price"] for row in data]

        plt.plot(dates, prices)
        plt.title("Monthly Expenses")
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.show()
