#experiment/base.py
from abc import ABC, abstractmethod

class Experiment(ABC):
    """
    Abstract base class for experiments.
    """

    @abstractmethod
    def run(self) -> None:
        """
        Run the experiment.
        """
        pass