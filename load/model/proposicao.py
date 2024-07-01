from datetime import datetime

from peewee import *


psql_db = PostgresqlDatabase(
    'postgres',
    user='postgres',
    password='example',
    host='localhost'
)


class BaseModel(Model):
    class Meta:
        database = psql_db


class Proposicao(BaseModel):
    proposicao_id: int = IntegerField()
    uri: str = CharField()
    sigla_tipo: str = CharField()
    ementa: str = TextField(null=True)
    data_apresentacao: datetime = DateTimeField()
    status_proposicao_despacho: str = TextField(null=True)
    status_proposicao_apreciacao: str = TextField(null=True)
    descricao_tipo: str = TextField(null=True)
    justificativa: str = TextField(null=True)


if __name__ == '__main__':
    tables = [Proposicao]
    with psql_db:
        psql_db.drop_tables(tables)
        psql_db.create_tables(tables)
