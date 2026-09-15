from datetime import datetime
from peewee import *

conexao = SqliteDatabase("agenda.db")

class Contato(Model):
    nome = CharField()
    telefone = CharField()
    data_cadastro = DateTimeField(default=datetime.now)

    def __str__(self):
        data_formatada = self.data_cadastro.strftime("%d/%m/%Y %H:%M:%S")
        return f"ID: {self.id} | Nome: {self.nome} | Telefone: {self.telefone} | Criado em: {data_formatada}"

    class Meta:
        database = conexao

conexao.connect()
conexao.create_tables([Contato])

def cadastrar_contato():
    print("CADASTRAR CONTATO")
    nome = input("Digite o nome: ").strip()
    telefone = input("Digite o telefone: ").strip()
    
    if nome and telefone:
        contato = Contato.create(nome=nome, telefone=telefone)
        print(f"Contato '{contato.nome}' cadastrado com sucesso!")
    else:
        print("Nome e telefone são obrigatórios.")

def ver_todos_contatos():
    print("TODOS OS CONTATOS")
    contatos = Contato.select()
    
    if contatos.exists():
        for contato in contatos:
            print(contato)
    else:
        print("Nenhum contato cadastrado até o momento.")

def buscar_contato():
    print("BUSCAR CONTATO")
    termo = input("Digite o nome (ou parte dele): ").strip()
    
    resultados = Contato.select().where(Contato.nome.contains(termo))
    
    if resultados.exists():
        print(f"Resultados encontrados ({resultados.count()}):")
        for contato in resultados:
            print(contato)
    else:
        print(f"Nenhum contato encontrado contendo '{termo}'.")

def editar_contato():
    print("EDITAR CONTATO")
    try:
        contato_id = int(input("Digite o ID do contato que deseja editar: "))
        contato = Contato.get_by_id(contato_id)
        
        print(f"Contato selecionado: {contato}")
        novo_nome = input(f"Novo nome (deixe em branco para manter '{contato.nome}'): ").strip()
        novo_telefone = input(f"Novo telefone (deixe em branco para manter '{contato.telefone}'): ").strip()
        
        if novo_nome:
            contato.nome = novo_nome
        if novo_telefone:
            contato.telefone = novo_telefone
            
        contato.save()
        print("Contato atualizado com sucesso!")
        
    except ValueError:
        print("ID inválido. Digite um número inteiro.")
    except Contato.DoesNotExist:
        print("Contato não encontrado para o ID informado.")

def excluir_contato():
    print("EXCLUIR CONTATO")
    try:
        contato_id = int(input("Digite o ID do contato a ser excluído: "))
        contato = Contato.get_by_id(contato_id)
        
        confirmacao = input(f"Tem certeza que deseja excluir '{contato.nome}'? (S/N): ").strip().upper()
        if confirmacao == 'S':
            contato.delete_instance()
            print("Contato excluído com sucesso!")
        else:
            print("Operação cancelada.")
            
    except ValueError:
        print("ID inválido. Digite um número inteiro.")
    except Contato.DoesNotExist:
        print("Contato não encontrado para o ID informado.")

def menu():
    while True:
        print("===== AGENDA DE CONTATOS =====")
        print("1 - Cadastrar contato")
        print("2 - Ver todos os contatos")
        print("3 - Buscar contato pelo nome")
        print("4 - Editar contato pelo ID")
        print("5 - Excluir contato pelo ID")
        print("6 - Sair")
        
        opcao = input("Escolha uma opção: ").strip()
        
        if opcao == '1':
            cadastrar_contato()
        elif opcao == '2':
            ver_todos_contatos()
        elif opcao == '3':
            buscar_contato()
        elif opcao == '4':
            editar_contato()
        elif opcao == '5':
            excluir_contato()
        elif opcao == '6':
            print("\nEncerrando a agenda. Até logo!")
            conexao.close()
            break
        else:
            print("Opção inválida! Tente novamente.")

if __name__ == '__main__':
    menu()