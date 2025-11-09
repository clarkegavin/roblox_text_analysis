# data/pipeline_factory.py
from typing import List, Optional, Type
from data.factory import ExtractorFactory
from pipelines.data_extractor_pipeline import DataExtractorPipeline
from data.models import Base, RobloxGame  # and any other models
from logs.logger import get_logger
import yaml
import inspect

from typing import List, Type
from logs.logger import get_logger
import yaml
import importlib

from pipelines.base import Pipeline

class PipelineFactory:
    """
    Factory for dynamically building pipelines from YAML.
    Supports arbitrary pipeline classes and parameters.
    """
    logger = get_logger("PipelineFactory")

    _registry = {}

    @classmethod
    def register_pipeline(cls, name: str, pipeline: Pipeline):
        cls._registry[name] = pipeline
        cls.logger.info(f"Registered pipeline: {name}")

    @classmethod
    def get_pipeline(cls, name: str) -> Pipeline:
        pipeline = cls._registry.get(name)
        if not pipeline:
            cls.logger.warning(f"Pipeline '{name}' not found in registry")
        return pipeline

    @classmethod
    def build_pipelines_from_yaml(cls, yaml_path: str) -> List[Pipeline]:
        """
        Build pipelines dynamically from a YAML configuration.
        Each YAML entry must include:
          - type: full class name (e.g., pipelines.data_extractor_pipeline.DataExtractorPipeline)
          - params: dict of parameters for the constructor
        """
        with open(yaml_path, "r") as f:
            config = yaml.safe_load(f)

        pipelines: List[Pipeline] = []

        for entry in config.get("pipelines", []):
            if not entry.get("enabled", True):
                cls.logger.info(f"Skipping disabled pipeline '{entry.get('name')}'")
                continue

            pipeline_type = entry.get("type")
            params = entry.get("params", {})

            extractor_type = entry.get("extractor_type")  # optional, indicates which extractor to create
            extractor_params = params.pop("extractor_params", {})  # remove extractor-specific params

            if not pipeline_type:
                cls.logger.warning(f"Pipeline type missing for '{entry.get('name')}', skipping")
                continue

            try:
                # Dynamically import the class
                module_name, class_name = pipeline_type.rsplit(".", 1)
                module = importlib.import_module(module_name)
                klass: Type[Pipeline] = getattr(module, class_name)
                # If an extractor type is specified, create the extractor
                # --- Create extractor if needed ---
                extractor = None
                if extractor_type:
                    if extractor_type == "roblox":
                        from data.factory import ExtractorFactory
                        extractor = ExtractorFactory.create_roblox_extractor(**extractor_params)
                    else:
                        # add other extractors here as needed
                        pass
                # Instantiate pipeline with parameters from YAML
                constructor_params = inspect.signature(klass.__init__).parameters
                if 'extractor' in constructor_params:
                    pipeline_instance = klass(extractor=extractor, **params)
                else:
                    pipeline_instance = klass(**params)
                #pipeline_instance = klass(extractor=extractor, **params)
                pipelines.append(pipeline_instance)
                cls.register_pipeline(entry.get("name"), pipeline_instance)

                cls.logger.info(f"Pipeline '{entry.get('name')}' ({pipeline_type}) created successfully")

            except Exception as e:
                cls.logger.error(f"Failed to create pipeline '{entry.get('name')}': {e}")

        return pipelines