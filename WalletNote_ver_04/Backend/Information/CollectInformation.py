class CollectInformation:
    def __init__(self, input_info):
        self.input_info = input_info

    def to_dict(self):
        return {
            "date": self.input_info.date,
            "amount": self.input_info.amount,
            "category": self.input_info.category,
            "type": self.input_info.type
        }
