from .base import Model
from sklearn.naive_bayes import GaussianNB

class NaiveBayesClassificationModel(Model):
    """
    Naive Bayes Classification Model.
    """

    def __init__(self, name: str, **params):
        super().__init__(name, **params)
        self.model = None
        self.params = params

    def build(self):
        self.model = GaussianNB(**self.params)
        self.logger.info(f"Built Naive Bayes model with params: {self.params}")
        return self
