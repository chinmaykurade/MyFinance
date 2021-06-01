from sklearn.pipeline import Pipeline

import logging
from myfinance.preprocess.preprocess import ExtractTablesAndInfos
from myfinance.score.score import ScoreStocks
import os


_logger = logging.getLogger(__name__)
MONGO_URI = os.environ.get('MONGO_URI')


stocks_pipe = Pipeline(
    [
        (
            "tables_infos_extractor",
            ExtractTablesAndInfos(mongo_uri=MONGO_URI, db='STOCKS_YF', collection_name='stocks_data'),
        ),
        (
            "scorer",
            ScoreStocks()
        )
    ]
)


