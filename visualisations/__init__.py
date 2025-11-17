#visualisations/__init__.py
from .bar_chart import BarChart
from .confusion_matrix_chart import ConfusionMatrixChart
from .word_cloud import WordCloudChart
from .factory import VisualisationFactory
from .base import Visualisation

# Register visualisations

VisualisationFactory.register_visualisation("confusion_matrix", ConfusionMatrixChart)
VisualisationFactory.register_visualisation("bar_chart", BarChart)
VisualisationFactory.register_visualisation("word_cloud", WordCloudChart)

__all__ = [
    "ConfusionMatrixChart",
    "VisualisationFactory",
    "Visualisation",
    "BarChart",
    "WordCloudChart"
]
