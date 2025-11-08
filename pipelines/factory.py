# data/pipeline_factory.py
from typing import List, Optional, Type
from data.factory import ExtractorFactory
from pipelines.table_pipeline import TablePipeline
from data.models import Base, RobloxGame  # and any other models
from logs.logger import get_logger
import yaml

class PipelineFactory:
    """
    Dynamically builds and registers pipelines based on a YAML configuration file.
    """
    _registry = {}
    _model_mapping = {
        "roblox_pipeline": RobloxGame,
        # Add other table pipelines here
        # "my_other_table": MyOtherModel,
    }

    logger = get_logger("PipelineFactory")

    @classmethod
    def register_pipeline(cls, name: str, pipeline: TablePipeline):
        cls._registry[name] = pipeline
        cls.logger.info(f"Registered pipeline: {name}")

    @classmethod
    def get_pipeline(cls, name: str) -> Optional[TablePipeline]:
        return cls._registry.get(name)

    @classmethod
    def build_pipelines_from_yaml(cls, yaml_path: str) -> List[TablePipeline]:
        """
        Build and register pipelines from a YAML config.
        Supports 'full' or 'sample' datasets.
        """
        with open(yaml_path, "r") as f:
            config = yaml.safe_load(f)

        pipelines = []

        for name, conf in config.items():
            if not conf.get("enabled", True):
                cls.logger.info(f"Skipping pipeline {name} (disabled)")
                continue

            model: Type[Base] = cls._model_mapping.get(name)
            if not model:
                cls.logger.warning(f"No model registered for pipeline '{name}', skipping")
                continue

            pipeline_type = conf.get("type", "full")
            sample_size = conf.get("sample_size") if pipeline_type == "sample" else None
            output_csv = conf.get("output_csv", f"{name}.csv")

            extractor = ExtractorFactory.create_custom_extractor(model, sample_size=sample_size)
            pipeline = TablePipeline(extractor, output_csv=output_csv)

            cls.register_pipeline(name, pipeline)
            pipelines.append(pipeline)

        return pipelines