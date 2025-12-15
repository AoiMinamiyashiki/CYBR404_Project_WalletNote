import matplotlib.pyplot as plt

class PieChart:
    def draw(self, data: dict):
        plt.pie(data.values(), labels=data.keys(), autopct="%1.1f%%")
        plt.show()
