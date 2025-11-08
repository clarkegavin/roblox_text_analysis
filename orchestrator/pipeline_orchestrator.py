# data/orchestrator.py
from typing import List
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from pipelines.table_pipeline import TablePipeline
from pipelines.factory import PipelineFactory
from logs.logger import get_logger

class PipelineOrchestrator:
    """
    Orchestrates execution of pipelines.
    Does not decide what pipelines exist — just runs them.
    """
    def __init__(self, pipelines: List[TablePipeline], max_retries: int = 3, parallel: bool = False):
        self.logger = get_logger(self.__class__.__name__)
        self.max_retries = max_retries
        self.parallel = parallel
        self.pipelines = pipelines

    def add_pipeline(self, pipeline: TablePipeline):
        self.pipelines.append(pipeline)

    def run_pipeline(self, pipeline: TablePipeline):
        attempt = 0
        while attempt < self.max_retries:
            try:
                self.logger.info(f"Running pipeline: {pipeline.__class__.__name__}, attempt {attempt+1}")
                pipeline.execute()
                self.logger.info(f"Pipeline {pipeline.__class__.__name__} completed successfully")
                return True
            except Exception as e:
                attempt += 1
                self.logger.error(f"Pipeline {pipeline.__class__.__name__} failed on attempt {attempt}: {e}")
                time.sleep(2)
        self.logger.error(f"Pipeline {pipeline.__class__.__name__} failed after {self.max_retries} attempts")
        return False

    def run(self):
        if self.parallel:
            self.logger.info("Running pipelines in parallel")
            with ThreadPoolExecutor(max_workers=len(self.pipelines)) as executor:
                futures = {executor.submit(self.run_pipeline, p): p for p in self.pipelines}
                for future in as_completed(futures):
                    _ = future.result()
        else:
            self.logger.info("Running pipelines sequentially")
            for pipeline in self.pipelines:
                self.run_pipeline(pipeline)