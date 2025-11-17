#eda/__init__.py
from .factory import EDAFactory
from .class_balance_eda import ClassBalanceEDA
from .wordcloud_eda import WordCloudEDA

EDAFactory.register_eda("class_balance", ClassBalanceEDA)
EDAFactory.register_eda("wordcloud_global", lambda: WordCloudEDA(per_class=False))
EDAFactory.register_eda("wordcloud_by_class", lambda: WordCloudEDA(per_class=True))


__all__ = [
    "EDAFactory",
    "ClassBalanceEDA",
    "WordCloudEDA",
]
