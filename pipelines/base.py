# pipelines/base.py
from abc import ABC, abstractmethod

class Pipeline(ABC):
    """
    Abstract base class for data processing pipelines.
    """

    @abstractmethod
    def execute(self) -> None:
        """
        Execute the data processing pipeline.
        """
        pass