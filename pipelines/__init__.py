from .data_splitter_pipeline import DataSplitterPipeline
from .factory import PipelineFactory
from .data_extractor_pipeline import DataExtractorPipeline

# Register pipelines
PipelineFactory.register_pipeline("data_extractor", DataExtractorPipeline)
PipelineFactory.register_pipeline("DataExtractorPipeline", DataSplitterPipeline)

__all__ = [
    "PipelineFactory",
    "data_extractor_pipeline",
    "data_splitter_pipeline"
]
