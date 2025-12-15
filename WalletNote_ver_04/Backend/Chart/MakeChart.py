import io
import matplotlib
matplotlib.use("Agg")  # サーバー描画用
import matplotlib.pyplot as plt

class MakeChart:
    def pie(self, data: dict, title: str = "") -> bytes:
        fig, ax = plt.subplots(figsize=(5, 5))
        ax.pie(
            data.values(),
            labels=data.keys(),
            autopct="%1.1f%%",
            startangle=90
        )
        ax.set_title(title)
        ax.axis("equal")

        buf = io.BytesIO()
        plt.tight_layout()
        plt.savefig(buf, format="png", dpi=150, transparent=True)
        plt.close(fig)
        buf.seek(0)
        return buf.read()

    def bar(self, data: dict, title: str = "") -> bytes:
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.bar(data.keys(), data.values())
        ax.set_title(title)
        ax.set_ylabel("Amount")
        ax.tick_params(axis='x', rotation=30)

        buf = io.BytesIO()
        plt.tight_layout()
        plt.savefig(buf, format="png", dpi=150, transparent=True)
        plt.close(fig)
        buf.seek(0)
        return buf.read()
