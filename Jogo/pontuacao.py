import datetime
from peewee import *

db = SqliteDatabase('ranking.db')

class BaseModel(Model):
    class Meta:
        database = db

class Pontuacao(BaseModel):
    nome_jogador = CharField()
    pontos = IntegerField()
    tempo_partida = FloatField()
    data_hora = DateTimeField(default=datetime.datetime.now)

def inicializar_banco():
    db.connect()
    db.create_tables([Pontuacao])