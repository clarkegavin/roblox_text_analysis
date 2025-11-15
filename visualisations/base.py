#visualisations/base.py
from abc import ABC, abstractmethod
from logs.logger import get_logger

class Visualisation(ABC):
    """
    Abstract base class for visualisations.
    """
    def __init__(self, title: str, figsize: tuple=(10,6)):
        self.title = title
        self.logger = get_logger(f"Visualisation:{title}")
        self.logger.info(f'Initialized visualisation: {title}')

    @abstractmethod
    def plot(self, data, **kwargs):
        """
        Create the visualisation.
        """
        pass


    def save(self, fig, filepath: str, dpi=300):
        """
        Save the visualisation to a file.
        """
        self.logger.info(f'Saving visualisation to {filepath}')
        fig.savefig(filepath, dpi=dpi, bbox_inches='tight')
        self.logger.info(f'Visualisation saved to {filepath}')
