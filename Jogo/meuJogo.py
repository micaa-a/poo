import arcade

class Player(arcade.Sprite):
    def __init__(self):
        super().__init__("Jogo/player_direita.png", scale=1)

        self.textura_direita = arcade.load_texture("Jogo/player_direita.png")
        self.textura_esquerda = arcade.load_texture("Jogo/player_esquerda.png")

    def update(self, delta_time):
        self.center_x += self.change_x
        self.center_y += self.change_y
        
        if self.change_x > 0:
            self.texture = self.textura_direita
        elif self.change_x < 0:
            self.texture = self.textura_esquerda

class Moeda(arcade.Sprite):
    def __init__(self):
        super().__init__("Jogo/moeda.png", scale = 0.9)

    def update(self, delta_time):
        self.center_x += self.change_x
        self.center_y += self.change_y 

        if self.right > 800:
            self.right = 800
            self.change_x = 0
        if self.top > 600:
            self.top = 600
            self.change_y = 0
        if self.left < 0:
            self.left = 0
            self.change_x = 0
        if self.bottom < 0:
            self.bottom = 0
            self.change_y = 0

class JanelaJogo(arcade.Window):
    def __init__(self):
        super().__init__(800, 600, "Jogo da Mica")
        arcade.set_background_color((54, 6, 6))

        self.velocidade = 2

        self.jogador = Player()
        self.jogador.center_x = 400
        self.jogador.center_y = 300
        self.sprite_jogador = arcade.SpriteList()
        self.sprite_jogador.append(self.jogador)

        self.moeda = Moeda()
        self.moeda.center_x = 500
        self.moeda.center_y = 260
        self.moeda.change_x = self.velocidade
        self.moeda.change_y = self.velocidade

        self.sprite_moeda = arcade.SpriteList()
        self.sprite_moeda.append(self.moeda)

    def on_draw(self):
        self.clear()

        self.sprite_jogador.draw()
        self.sprite_moeda.draw()

    def on_update(self, delta_time):
        self.sprite_jogador.update(delta_time)
        self.sprite_moeda.update(delta_time)

def main():
    tela = JanelaJogo()
    arcade.run()
if __name__ == "__main__":
    main()

