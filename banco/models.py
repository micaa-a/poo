#importar bibliotecas
import datetime
from peewee import *

#definir onde está o banco de dados (arquivo local)
conexao = SqliteDatabase("models.db")

#criar minha classe de contato
class Contato(Model):

    #definir os atributos dela
    nome = CharField()
    telefone = CharField()

    #sobreescrever o método que imprime o objeto inteiro
    def __str__(self):
        return f"{self.nome}: {self.telefone}"

    #criar uma classe metadados para definir em qual banco será criado uma tabela para esta classe
    class Meta:
        database = conexao

#depois de criar todas as classes, vamos conectar no banco de dados
conexao.connect()

#pedir para a conexão criar as tabelas das classes, caso não existam
conexao.create_tables( [Contato] )


