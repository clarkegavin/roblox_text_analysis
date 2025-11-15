#visualisations/__init__.py
from .confusion_matrix_chart import ConfusionMatrixChart
from .factory import VisualisationFactory
from .base import Visualisation

# Register visualisations

VisualisationFactory.register_visualisation("confusion_matrix", ConfusionMatrixChart)

__all__ = [
    "ConfusionMatrixChart",
    "VisualisationFactory",
    "Visualisation",
]
