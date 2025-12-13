from RecallDB import RecallDB
from MakeGraph import MakeGraph


class Dashboard:
    """
    Dashboard controller.
    """

    def show(self):
        data = RecallDB().fetch_all()
        MakeGraph().monthly_graph()
        return data
