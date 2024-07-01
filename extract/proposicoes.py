import asyncio
from datetime import datetime
import pytz

from common.utils import CamaraSession, create_dirs

import pandas as pd

from extract.common.logger import get_logger
from extract.model.proposicao import proposicao_mapping, Proposicao

log = get_logger()
camara_api = CamaraSession()

TZ = pytz.timezone("America/Sao_Paulo")
DEST_PATH = "/tmp/camara_files"


async def get_lista_proposicoes(data_inicio) -> list:
    result = await camara_api.get(f"https://dadosabertos.camara.leg.br/api/v2/proposicoes?dataInicio={data_inicio}")
    ids = [i["id"] for i in result["dados"]]
    return ids


async def get_proposicao(proposicao_id: int) -> Proposicao:
    log.info(f"Coletando proposicao {proposicao_id}")
    r = await camara_api.get(f"https://dadosabertos.camara.leg.br/api/v2/proposicoes/{proposicao_id}")
    proposicao_json = r["dados"]
    proposicao_df = pd.json_normalize(proposicao_json, sep="_").rename(columns=proposicao_mapping)
    return Proposicao(proposicao_df)


async def extract_proposicoes(data_inicio: str = None):
    if not data_inicio:
        data_inicio = datetime.now(TZ).date().isoformat()

    proposicoes_ids = await get_lista_proposicoes(data_inicio)
    for proposicao_id in proposicoes_ids:
        proposicao = await get_proposicao(proposicao_id)
        proposicao.to_parquet(f"{DEST_PATH}/{proposicao_id}.parquet", mkdirs=create_dirs)


if __name__ == '__main__':
    asyncio.run(extract_proposicoes("2024-06-03"))
