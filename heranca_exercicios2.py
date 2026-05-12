from heranca_exercicios import Calculadora, CalculadoraCientifica

marca = input("Digite a marca da calculadora:")
modelo = input("Digite o modelo da calculadora:")
ano = input("Digite o ano da calculadora:")
calc = Calculadora(marca, modelo, ano)

num1 = int(input("Digite o primeiro número:"))
num2 = int(input("Digite o segundo número:"))

print ("Soma:" + str(calc.Somar(num1, num2)))
print ("Subtração:" + str(calc.Subtrair(num1, num2)))
print ("Multiplicação:" + str(calc.Multiplicar(num1, num2)))
print ("Divisão:" + str(calc.Divisao(num1, num2)))
