class Aluno:
    def __init__(self, nome, idade, curso, notas):
        self.nome = nome
        self.idade = idade
        self.curso = curso 
        self.notas = notas

    def apresentar(self):
        print(f"Olá, meu nome é {self.nome}, tenho {self.idade} anos e faço o curso de {self.curso}.")

    def calcular_media(self):
        media = round(sum(self.notas) / 3, 2)       
        return print(f"A média deste aluno é: {media}")

nome = input("Digite o nome do aluno:")
idade = input("Digite a idade do aluno:")
curso = input("Digite o curso do aluno:")
notas = []
for i in range(3):
    nota = float (input(f"Digite a nota {i+1}:"))
    notas.append(nota)

aluno1 = Aluno(nome, idade, curso, notas)
aluno1.apresentar()
aluno1.calcular_media()