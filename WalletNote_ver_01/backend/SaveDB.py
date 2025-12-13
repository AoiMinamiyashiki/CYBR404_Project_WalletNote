import csv


class SaveDB:
    """
    Save data to external files.
    """

    def save_csv(self, data, filename="records.csv"):
        if not data:
            return

        with open(filename, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
