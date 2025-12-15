class MonthlyReport:
    def summarize(self, records):
        summary = {}
        for r in records:
            month = r["date"].strftime("%Y-%m")
            summary[month] = summary.get(month, 0) + r["amount"]
        return summary
