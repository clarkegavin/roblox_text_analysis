from .base import EDAComponent
from logs.logger import get_logger
from visualisations.factory import VisualisationFactory
import os

class ClassBalanceEDA(EDAComponent):
    """
    EDA component to analyze and visualize class balance in the target variable.
    """

    def __init__(self):
        self.logger = get_logger("ClassBalanceEDA")
        self.logger.info("Initialized ClassBalanceEDA component")

    def run(self, data, target, text_field=None, save_path=None,**kwargs):
        """
        Analyze and visualize class balance in the target variable.

        Parameters:
        - data: The dataset containing the target variable.
        - target: The name of the target variable column.
        - text_field: Not used in this component.
        - kwargs: Additional parameters for visualization.

        Returns:
        - fig: The generated class balance plot.
        """
        self.logger.info(f"Running ClassBalanceEDA on target: {target}")

        # Calculate class distribution
        class_counts = data[target].value_counts().to_dict()
        self.logger.info(f"Class distribution: {class_counts}")
        filepath = os.path.join(save_path, "class_balance.png")

        # viz = VisualisationFactory.get_visualisation("bar_chart")
        # viz.plot(
        #     #data=class_counts,
        #     title="Class Balance",
        #     xlabel=target,
        #     ylabel="Count",
        #     #save_path=filepath
        # )
        viz = VisualisationFactory.get_visualisation(
            "bar_chart",
            title="Class Balance",
            xlabel=target,
            ylabel="Count",
            figsize=(10, 6)
        )

        fig, ax = viz.plot(data=class_counts)
        viz.save(fig, filepath)
        return filepath