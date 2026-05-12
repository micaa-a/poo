from aula_heranca_classes import Animal, Gato, Cachorro

ginger = Gato("Ginger", "Laranja", 4)
print(f"Meu gato é o {ginger.nome}")
ginger.respirar()
ginger.ronronar()
ginger.rugir()

print("--------------------------------")

floki = Cachorro("Floki", "Vira-lata", 4)
print(f"Meu cachorro é o {floki.nome}")
floki.abanar_rabo()
floki.respirar()
floki.rugir()