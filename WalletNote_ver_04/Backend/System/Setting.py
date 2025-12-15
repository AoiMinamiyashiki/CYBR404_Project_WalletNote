class Setting:
    def __init__(self, currency="USD", theme="GoldBlack"):
        self.currency = currency
        self.theme = theme

    def get_settings(self):
        return {
            "currency": self.currency,
            "theme": self.theme
        }
