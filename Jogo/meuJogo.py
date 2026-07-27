import arcade
import random 

class Player(arcade.Sprite):
    def __init__(self):
        super().__init__("player_direita.png", scale=1)

        self.textura_direita = arcade.load_texture("player_direita.png")
        self.textura_esquerda = arcade.load_texture("player_esquerda.png")

    def update(self, delta_time):
        self.center_x += self.change_x
        self.center_y += self.change_y
        
        if self.change_x > 0:
            self.texture = self.textura_direita
        elif self.change_x < 0:
            self.texture = self.textura_esquerda

        if self.right > 800:
            self.right = 800
            self.change_x = 0
        if self.top > 600:
            self.top = 600
            self.change_y = 0
        if self.left < 0:
            self.change_x = 0
            self.left = 0
        if self.bottom < 0:
            self.bottom = 0
            self.change_y = 0

class Inimigo(arcade.Sprite):
    def __init__(self):
        super().__init__("inimigo.png", scale = 1.5)

    def aplicar_efeito(self, jogo):
        jogo.pontuacao -= 1

    def update(self, delta_time):
            self.center_x += self.change_x
            self.center_y += self.change_y
    
            if self.right > 800 or self.left < 0:
                self.change_x *= -1
            if self.top > 600 or self.bottom < 0:
                self.change_y *= -1

class Moeda(arcade.Sprite):
    def __init__(self):
        super().__init__("moeda.png", scale = 0.9)

    def update(self, delta_time):
        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.right > 800 or self.left < 0:
            self.change_x = 0 
        if self.top > 600 or self.bottom < 0:
            self.change_y = 0 

class MoedaEspecial(arcade.Sprite):
    def __init__(self):
        super().__init__("moeda.png", scale = 0.9)

    def update(self, delta_time):
        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.right > 800 or self.left < 0:
                self.change_x *= -1
        if self.top > 600 or self.bottom < 0:
                self.change_y *= -1

class JanelaJogo(arcade.Window):
    def __init__(self):
        super().__init__(800, 600, "Jogo da Mica")
        arcade.set_background_color((54, 6, 6))

        self.velocidade = 3

        self.setup()

    def setup(self):
        self.tempo = 0
        self.jogo_finalizado = False
        self.pontuacao = 0 

        self.jogador = Player()
        self.jogador.left = 0
        self.jogador.bottom = 0       

        self.sprite_jogador = arcade.SpriteList()
        self.sprite_jogador.append(self.jogador)

        self.inimigo = Inimigo()
        self.inimigo.center_x = 150
        self.inimigo.center_y = 100
        self.inimigo.change_x = self.velocidade
        self.inimigo.change_y = self.velocidade-1
        self.sprite_inimigos = arcade.SpriteList()
        self.sprite_inimigos.append(self.inimigo)

        self.moeda = Moeda()
        self.moeda.center_x = 150
        self.moeda.center_y = 100
        self.sprite_moeda = arcade.SpriteList()
        self.sprite_moeda.append(self.moeda)

        self.moeda_especial = MoedaEspecial()
        self.moeda_especial.center_x = 650
        self.moeda_especial.center_y = 500
        self.moeda_especial.change_x = self.velocidade
        self.moeda_especial.change_y = self.velocidade-1
        self.sprite_moeda.append(self.moeda_especial)

        for i in range (25):
            self.moeda_simples = Moeda()
            self.moeda_simples.center_x = random.randint(50, 750)
            self.moeda_simples.center_y = random.randint(50, 550)
            self.sprite_moeda.append(self.moeda_simples)

    def on_draw(self):
        self.clear()

        self.sprite_jogador.draw()
        self.sprite_moeda.draw()
        self.sprite_inimigos.draw()

        arcade.draw_text(f"Tempo: {self.tempo:.2f}s", 10, 570, arcade.color.WHITE, 20)

        arcade.draw_text(f"Pontuação: {self.pontuacao}", 10, 540, arcade.color.WHITE, 20)

        if self.jogo_finalizado:
            arcade.draw_text("FIM DE JOGO", 400, 450, arcade.color.YELLOW, 30, anchor_x="center")

            arcade.draw_text(f"Pontuação final: {self.pontuacao}", 400, 350, arcade.color.WHITE, 20, anchor_x="center")

            arcade.draw_text(f"Tempo final: {self.tempo:.2f}s", 400, 300, arcade.color.WHITE, 20, anchor_x="center")

            arcade.draw_text("Pressione R para recomeçar", 400, 200, arcade.color.GREEN, 16, anchor_x="center")

            arcade.draw_text("Pressione ESC para sair", 400, 160, arcade.color.RED, 16, anchor_x="center")

    def on_update(self, delta_time):

        if not self.jogo_finalizado:
            self.tempo += delta_time

            self.sprite_jogador.update(delta_time)
            self.sprite_moeda.update(delta_time)
            self.sprite_inimigos.update(delta_time)

            moedas_colididas = arcade.check_for_collision_with_list(self.jogador, self.sprite_moeda)
            for moeda in moedas_colididas:
                moeda.remove_from_sprite_lists()
                if moeda == self.moeda_especial:
                    self.pontuacao += 5
                else:
                    self.pontuacao += 1

            inimigos_colididos = arcade.check_for_collision_with_list(self.jogador, self.sprite_inimigos)
            for inimigo in inimigos_colididos:
                    inimigo.aplicar_efeito(self)

            if len(self.sprite_moeda) == 0:
                self.jogo_finalizado = True

    def on_key_press(self, key, modifiers):
        if key == arcade.key.A: 
            self.jogador.change_x = -self.velocidade
        elif key == arcade.key.D:
            self.jogador.change_x = self.velocidade
        elif key == arcade.key.W:
            self.jogador.change_y = self.velocidade
        elif key == arcade.key.S:
            self.jogador.change_y = -self.velocidade

        if key == arcade.key.ESCAPE:
            self.close()

        if key == arcade.key.R:
            self.setup()    

    def on_key_release(self, key, modifiers):
        if key == arcade.key.A or key == arcade.key.D:
            self.jogador.change_x = 0
        elif key == arcade.key.W or key == arcade.key.S:
            self.jogador.change_y = 0

def main():
    tela = JanelaJogo()
    arcade.run()

if __name__ == "__main__":
    main()