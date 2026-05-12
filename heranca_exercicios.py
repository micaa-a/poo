import math

class Calculadora:
    def __init__(self, marca, modelo, ano):
        self.marca = marca
        self.modelo = modelo
        self.ano = ano

    def Somar(self, a, b, c=0):
        soma = a + b + c
        return soma
    
    def Subtrair(self, a, b, c=0):
        subtracao = a - b - c
        return subtracao

    def Multiplicar(self, a, b, c=1):
        multiplicacao = a * b * c
        return multiplicacao

    def Divisao (self, a, b):
        if(b == 0):
            print("Não é possível dividir")
        else:
            divisao = a / b 
            return divisao

class CalculadoraCientifica(Calculadora):
    def __init__(self, funcoes_cientificas):
        super().__init__()

    def Potencia(self, base, expoente):
        potencia = base ** expoente
        print(potencia)

    def Raiz_quadrada(self, numero):
        raiz = math.sqrt(numero)
        print(raiz)