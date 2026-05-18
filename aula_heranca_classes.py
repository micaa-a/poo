class Animal:
    def __init__(self, nome, especie, patas):
        self.nome = nome
        self.especie = especie
        self.patas = patas 

    def respirar(self):
        print ("Respirando")

    def rugir(self):
        print ("O animal vai rugir")

class Cachorro(Animal):
    def abanar_rabo(self):
        print("Abanando rabo")

    def rugir(self):
        print ("AUAUAUAUAUA")

class Gato(Animal):
    def __init__(self, dono):
        super().__init__()
        self.dono = dono

    def ronronar(self):
        print ("Ronronando")
        
    def rugir(self):
        print("MIAAAAAAAAAAAAAAAAAAAAU")
