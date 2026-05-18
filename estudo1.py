class Livro:
    def __init__(self, titulo, disponivel = True):
        self.titulo = titulo
        self.disponivel = disponivel

    def emprestar(self):
        if(self.disponivel):
            self.disponivel = False
            print("Livro emprestado com sucesso!")
        else:
            print("Livro já esta emprestado")

    def devolver(self):
        self.disponivel = True
        print("Livro devolvido com sucesso!")

livro = Livro("Dom casmurro")
livro.emprestar()
livro.emprestar()
livro.devolver()