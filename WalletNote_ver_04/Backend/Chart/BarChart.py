import matplotlib.pyplot as plt

class BarChart:
    def draw(self, data: dict):
        plt.bar(data.keys(), data.values())
        plt.show()
