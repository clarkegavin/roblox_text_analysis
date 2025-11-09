# orchestrator/pipeline_orchestrator.py
from typing import List
from logs.logger import get_logger

class PipelineOrchestrator:
    def __init__(self, pipelines: List, max_retries: int = 3, parallel: bool = False):
        self.logger = get_logger(self.__class__.__name__)
        self.pipelines = pipelines
        self.max_retries = max_retries
        self.parallel = parallel

    def run_pipeline(self, pipeline, data=None):
        attempt = 0
        while attempt < self.max_retries:
            try:
                self.logger.info(f"Running pipeline: {pipeline.__class__.__name__}, attempt {attempt+1}")
                result = pipeline.execute(data)
                self.logger.info(f"Pipeline {pipeline.__class__.__name__} completed successfully")
                return result
            except Exception as e:
                attempt += 1
                self.logger.error(f"Pipeline {pipeline.__class__.__name__} failed: {e}")
        self.logger.error(f"Pipeline {pipeline.__class__.__name__} failed after {self.max_retries} attempts")
        return False

    def run(self):
        self.logger.info("Starting orchestrator run")
        data = None
        for pipeline in self.pipelines:
            data = self.run_pipeline(pipeline, data)
            self.logger.info(f"Pipeline orchestration complete:  {pipeline.__class__.__name__}")
