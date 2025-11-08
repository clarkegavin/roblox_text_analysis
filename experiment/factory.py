#experiment/factory.py
from logs.logger import get_logger

class ExperimentFactory:
    """
    Factory for managing experiments.
    """
    _registry = {}

    logger = get_logger("ExperimentFactory")

    @classmethod
    def register_experiment(cls, name: str, experiment):
        cls._registry[name] = experiment
        cls.logger.info(f"Registered experiment: {name}")

    @classmethod
    def get_experiment(cls, name: str, **kwargs):
        experiment = cls._registry.get(name)
        if not experiment:
            cls.logger.warning(f"Experiment '{name}' not found in registry")
        return experiment(**kwargs) if experiment else None