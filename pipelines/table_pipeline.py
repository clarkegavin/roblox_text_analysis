# pipelines/table_pipeline.py
from typing import Optional
import os
import pandas as pd
from data.extractor import DataExtractor
from logs.logger import get_logger
from pipelines.base import Pipeline


class TablePipeline(Pipeline):
    """
    ETL pipeline for a single table extractor.
    Inherits from the base Pipeline class.
    """

    def __init__(self, extractor: DataExtractor, output_csv: Optional[str] = None):
        self.extractor = extractor
        self.logger = get_logger(self.__class__.__name__)
        self.df = None
        self.output_csv = output_csv or os.getenv("OUTPUT_CSV", "output.csv")

    def extract(self) -> None:
        """Extract data using the configured DataExtractor."""
        self.logger.info("Starting data extraction")
        self.df = pd.DataFrame(self.extractor.fetch_all())
        self.logger.info(f"Extracted {len(self.df)} rows")

    def transform(self) -> None:
        """Perform any data transformations."""
        self.logger.info("Starting transformation")

        # Example: parse datetime columns if present
        for col in ("Date", "Date_Created", "Last_Updated"):
            if col in self.df.columns:
                self.df[col] = pd.to_datetime(self.df[col], errors="coerce")

        self.logger.info("Transformation complete")

    def load(self) -> None:
        """Save transformed data to CSV."""
        self.logger.info(f"Saving data to {self.output_csv}")
        self.df.to_csv(self.output_csv, index=False)
        self.logger.info("Data saved successfully")

    def execute(self) -> None:
        """
        Execute the full ETL process.
        This method implements the abstract `execute()` from the base class.
        """
        self.extract()
        self.transform()
        self.load()
        self.logger.info("Pipeline execution complete")
