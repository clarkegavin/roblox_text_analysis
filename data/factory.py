# factory.py (refactored)
from typing import Optional, Type
from .sqlalchemy_connector import SQLAlchemyConnector
from .table_extractor import TableDataExtractor
from .abstract_connector import DBConnector
from .models import RobloxGame
from sqlalchemy.orm import DeclarativeMeta


class ExtractorFactory:
    """
    Factory for building table extractors.
    """

    @staticmethod
    def create_roblox_extractor(
        connector: Optional[DBConnector] = None,
        db_url: Optional[str] = None,
        sample_size: Optional[int] = None
    ) -> TableDataExtractor:
        """
        Returns a TableDataExtractor for RobloxGame table.
        """
        if connector is None:
            connector = SQLAlchemyConnector(db_url=db_url)
        return TableDataExtractor(connector, RobloxGame, sample_size=sample_size)

    @staticmethod
    def create_custom_extractor(
        model: Type[DeclarativeMeta],
        connector: Optional[DBConnector] = None,
        db_url: Optional[str] = None,
        sample_size: Optional[int] = None
    ) -> TableDataExtractor:
        """
        Returns a TableDataExtractor for any ORM model.
        """
        if connector is None:
            connector = SQLAlchemyConnector(db_url=db_url)
        return TableDataExtractor(connector, model, sample_size=sample_size)
