import pandera as pa


class BaseModel(pa.DataFrameModel):
    class Config:
        strict = "filter"


class Proposicao(BaseModel):
    proposicao_id: int = pa.Field()
    uri: str = pa.Field()
    sigla_tipo: str = pa.Field(nullable=True)
    ementa: str = pa.Field(nullable=True)
    data_apresentacao: pa.DateTime = pa.Field(coerce=True)
    status_proposicao_despacho: str = pa.Field(nullable=True)
    status_proposicao_apreciacao: str = pa.Field(nullable=True)
    descricao_tipo: str = pa.Field(nullable=True)
    justificativa: str = pa.Field(nullable=True)


proposicao_mapping = {
    "id": "proposicao_id",
    "siglaTipo": "sigla_tipo",
    "dataApresentacao": "data_apresentacao",
    "statusProposicao_despacho": "status_proposicao_despacho",
    "statusProposicao_apreciacao": "status_proposicao_apreciacao",
    "descricaoTipo": "descricao_tipo",
}
