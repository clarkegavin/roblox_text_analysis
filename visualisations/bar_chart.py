#visualisations/bar_chart.py
from .base import Visualisation
from logs.logger import get_logger

class BarChart(Visualisation):
    """
    Bar Chart Visualisation.
    """

    def __init__(self, title: str, xlabel=None, ylabel=None, figsize=(10,6), **params):
        super().__init__(title=title, figsize=figsize)
        self.logger = get_logger(self.__class__.__name__)
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.figsize = figsize
        self.params = params  # optional style parameters
        self.logger.info(f"Initialized Bar Chart visualisation with title: {title}, xlabel: {xlabel}, ylabel: {ylabel}, figsize: {figsize}, params: {params}")

    def build(self):
        self.logger.info(f"Built Bar Chart visualisation with params: {self.params}")
        return self


    def plot(self, data):
        import matplotlib.pyplot as plt

        self.logger.info(f"Creating Bar Chart visualisation with data: {data} ")
        # # Extract title so it doesn't get passed to ax.bar()
        # title = kwargs.pop("title", self.title)
        #
        # fig, ax = plt.subplots(figsize=self.params.get('figsize', (10, 6)))
        # ax.bar(data.keys(), data.values(), **kwargs)
        # ax.set_title(self.title)

        fig, ax = plt.subplots(figsize=self.figsize)

        # Only draw, no extra kwargs
        ax.bar(data.keys(), data.values())

        # Apply labels / title
        ax.set_title(self.title)
        if self.xlabel:
            ax.set_xlabel(self.xlabel)
        if self.ylabel:
            ax.set_ylabel(self.ylabel)

        rotation = self.params.get("xticks_rotation")
        if rotation is not None:
            ax.tick_params(axis='x', labelrotation=rotation)

        self.logger.info("Bar Chart visualisation created")
        return fig, ax
