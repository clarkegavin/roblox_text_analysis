# pipelines/base.py
from abc import ABC, abstractmethod
from typing import Any, Optional
import pandas as pd


class Pipeline(ABC):
    """
    Abstract base class for data processing pipelines.
    """

    @abstractmethod
    def execute(self, data: Optional[pd.DataFrame] = None) -> Any:
        """
        Execute the pipeline stage.

        Parameters
        ----------
        data : Optional[pd.DataFrame]
            Input data for this pipeline stage (if applicable).

        Returns
        -------
        Any
            Output of the pipeline stage (e.g., DataFrame, tuple of splits, model, etc.)
        """
        pass