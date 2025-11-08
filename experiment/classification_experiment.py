from base import Experiment
from logs.logger import get_logger
from sklearn.model_selection import train_test_split
import mlflow

class ClassificationExperiment(Experiment):
    """
    Concrete experiment class for classification tasks.
    """

    def __init__(self, name, model, evaluator, X, y, test_size=0.2):
        self.name = name
        self.model = model
        self.evaluator = evaluator
        self.X = X
        self.y = y
        self.test_size = test_size
        self.logger = get_logger(f"ClassificationExperiment.{self.name}")

    def run(self):
        self.logger.info(f"Starting classification experiment '{self.name}'")

        X_train, X_test, y_train, y_test = train_test_split(
            self.X, self.y, test_size=self.test_size, random_state=42
        )

        with mlflow.start_run(run_name=self.name):
            self.model.fit(X_train, y_train)
            y_pred = self.model.predict(X_test)

            metrics = self.evaluator.evaluate(y_test, y_pred)
            mlflow.log_params(self.model.get_params())
            mlflow.log_metrics(metrics)

        self.logger.info(f"Completed experiment '{self.name}' → {metrics}")
        return metrics
