from .factory import ModelFactory
from . import naive_bayes_model
from .naive_bayes_model import NaiveBayesClassificationModel

# Register models
ModelFactory.register_model("naive_bayes", NaiveBayesClassificationModel)

__all__ = [
    "ModelFactory",
    "naive_bayes_model",]
