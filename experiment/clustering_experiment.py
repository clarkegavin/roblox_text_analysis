from base import Experiment
from logs.logger import get_logger
import mlflow

class ClusteringExperiment(Experiment):
    """
    Concrete experiment class for clustering tasks.
    """

    def __init__(self, name, model, evaluator, X):
        self.name = name
        self.model = model
        self.evaluator = evaluator
        self.X = X
        self.logger = get_logger(f"ClusteringExperiment.{self.name}")

    def run(self):
        self.logger.info(f"Starting clustering experiment '{self.name}'")

        with mlflow.start_run(run_name=self.name):
            self.model.fit(self.X)
            labels = self.model.predict(self.X)

            metrics = self.evaluator.evaluate(self.X, labels)
            mlflow.log_params(self.model.get_params())
            mlflow.log_metrics(metrics)

        self.logger.info(f"Completed experiment '{self.name}' → {metrics}")
        return metrics
