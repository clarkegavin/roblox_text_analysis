# pipelines/data_cleanup_pipeline.py
from typing import Any, Dict, List, Optional
import pandas as pd
from pipelines.base import Pipeline
from preprocessing.factory import PreprocessorFactory
from logs.logger import get_logger


class DataCleanupPipeline(Pipeline):
    """Pipeline to run data cleanup preprocessors sequentially.

    Example config in YAML:
    cleanup_steps:
      - name: remove_duplicates
        params:
          field: "Genre"
          keep: "first"

    The pipeline creates each preprocessor via PreprocessorFactory and calls
    fit/transform similarly to PreprocessingPipeline but operates on the full
    DataFrame so cleanup steps can modify rows/columns.
    """

    def __init__(self, cleanup_steps: List[Dict[str, Any]]):
        self.logger = get_logger(self.__class__.__name__)
        self.logger.info("Initializing DataCleanupPipeline")
        self.cleanup_steps = cleanup_steps or []
        # build preprocessor instances
        self.steps = [
            PreprocessorFactory.create(step["name"], **step.get("params", {}))
            for step in self.cleanup_steps
        ]
        self.logger.info(f"Initialized {len(self.steps)} cleanup steps")
        self.logger.info(f"Raw cleanup steps config: {self.cleanup_steps}")

    @classmethod
    def from_config(cls, cfg: Dict[str, Any]) -> "DataCleanupPipeline":
        #steps = cfg.get("cleanup_steps", [])
        # Handle both direct and nested "params"
        params = cfg.get("params", cfg)
        steps = params.get("cleanup_steps", [])
        return cls(steps)

    def execute(self, data: Optional[pd.DataFrame] = None) -> Optional[pd.DataFrame]:
        self.logger.info("Executing DataCleanupPipeline")
        if data is None:
            self.logger.warning("No data provided to DataCleanupPipeline.execute; returning None")
            return None
        df = data
        for step in self.steps:
            try:
                self.logger.info(f"Applying cleanup step: {step.__class__.__name__}")
                step.fit(df)
                df = step.transform(df)
                # ensure df stays a DataFrame where reasonable
                if hasattr(df, "reset_index"):
                    try:
                        df = df.reset_index(drop=True)
                    except Exception:
                        pass
            except Exception as e:
                self.logger.exception(f"Cleanup step {step} failed: {e}")
        self.logger.info(f"DataCleanupPipeline completed - data shape: {getattr(df, 'shape', 'unknown')}")
        return df

