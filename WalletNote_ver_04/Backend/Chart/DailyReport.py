class DailyReport:
    def summarize(self, records):
        summary = {}
        for r in records:
            summary[r["category"]] = summary.get(r["category"], 0) + r["amount"]
        return summary
