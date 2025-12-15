class CategorySummary:
    def summarize(self, records: list, record_type: str = None) -> dict:
        """
        records: RecallDatabase.fetch_by_user() の結果
        record_type: 'income' / 'expense' / None(両方)
        """
        summary = {}
        for r in records:
            if record_type and r["type"] != record_type:
                continue
            cat = r["category"]
            summary[cat] = summary.get(cat, 0) + float(r["amount"])
        return summary
