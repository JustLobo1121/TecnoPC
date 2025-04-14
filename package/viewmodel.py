from .model import Model

class ViewModel:
    def __init__(self, model: Model):
        self.model = model

    def get_data(self):
        return self.model.get_data()
