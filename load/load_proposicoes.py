from datetime import datetime
from pathlib import Path

import pandas as pd
import pytz

from load.common.logger import get_logger
from load.model.proposicao import Proposicao, psql_db

log = get_logger()

TZ = pytz.timezone("America/Sao_Paulo")
SOURCE_PATH = "/tmp/camara_files"


def load_proposicao(proposicao_df: pd.DataFrame):
    proposicao_data = proposicao_df.to_dict("records")
    for proposicao in proposicao_data:
        with psql_db.atomic():
            Proposicao.create(**proposicao)


def load_proposicoes(data_inicio: str = None):
    if not data_inicio:
        data_inicio = datetime.now(TZ).date().isoformat()

    parquet_files = Path(SOURCE_PATH).glob('*.parquet')
    for parquet_file in parquet_files:
        proposicao_df = pd.read_parquet(parquet_file)
        load_proposicao(proposicao_df)


if __name__ == '__main__':
    load_proposicoes()
