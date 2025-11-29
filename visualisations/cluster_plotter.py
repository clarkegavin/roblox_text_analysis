# visualisations/cluster_plotter.py
import matplotlib.pyplot as plt
from .base import Visualisation
from logs.logger import get_logger
import os
import pandas as pd

class ClusterPlotter(Visualisation):
    """
    Cluster scatter plot visualisation.
    """

    def __init__(self, name: str = "cluster_plot",  title="Cluster Visualisation", xlabel=None, ylabel=None, figsize=(10, 6), **params):
        super().__init__(title=title, figsize=figsize)
        self.logger = get_logger(self.__class__.__name__)
        self.name = name
        self.title = title
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.figsize = figsize
        self.params = params  # optional style parameters
        self.save_path = params.get("output_dir", ".")
        self.logger.info(
            f"Initialized ClusterPlotter with title={title}, xlabel={xlabel}, ylabel={ylabel}, figsize={figsize}, params={params}"
        )

    def build(self):
        self.logger.info(f"Built ClusterPlotter with params: {self.params}")
        return self

    def plot(self, X_reduced, labels, **kwargs):
        """
        Plot 2D cluster scatter plot.

        Parameters:
            X_reduced: np.ndarray of shape (n_samples, 2)
            labels: cluster labels for each sample
            kwargs: optional style overrides (e.g., cmap, alpha)
        """
        self.logger.info(f"Creating cluster plot with {X_reduced.shape[0]} points")

        fig, ax = plt.subplots(figsize=self.figsize)
        scatter = ax.scatter(
            X_reduced[:, 0], X_reduced[:, 1], c=labels, **kwargs
        )

        ax.set_title(self.title)
        if self.xlabel:
            ax.set_xlabel(self.xlabel)
        if self.ylabel:
            ax.set_ylabel(self.ylabel)

        # Optional: xticks / yticks rotation from params
        rotation = self.params.get("xticks_rotation")
        if rotation is not None:
            ax.tick_params(axis='x', labelrotation=rotation)

        self.logger.info("Cluster plot created")
        return fig, ax, scatter

    def save_embeddings(self, X_embedded, labels, df_original, prefix="embedding"):
        """
        Save reduced coordinates + cluster labels + original metadata.
        """
        self.logger.info(f"Saving embeddings with prefix '{prefix}'")

        # Convert array → dataframe
        if X_embedded.shape[1] == 2:
            reduced_df = pd.DataFrame(X_embedded, columns=["x", "y"])
        elif X_embedded.shape[1] == 3:
            reduced_df = pd.DataFrame(X_embedded, columns=["x", "y", "z"])
        else:
            raise ValueError("X_embedded must be 2D or 3D for plotting.")

        # Add cluster labels
        reduced_df["cluster"] = labels

        # Add metadata from the original df (optional)
        # meta_cols = ["gameID", "Name", "Genre"]
        # for col in meta_cols:
        #     if col in df_original.columns:
        #         reduced_df[col] = df_original[col].values

        # Save to CSV
        out_path = os.path.join(self.output_dir, f"{prefix}.csv")
        reduced_df.to_csv(out_path, index=False)

        self.logger.info(f"Saved embedding CSV to {out_path}")
        return out_path