from .model import Model

class ViewModel:
    def __init__(self, model: Model):
        self._model = model

    def get_data(self):
        return self._model.get_data()