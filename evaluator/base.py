from abc import ABC, abstractmethod

class Evaluator(ABC):
    """
    Abstract base class for model evaluators.
    """

    @abstractmethod
    def evaluate(self, y_true, y_pred, prefix: str ='') -> dict:
        """
        Evaluate the model predictions against true values.
        """
        pass