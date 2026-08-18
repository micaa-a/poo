import arcade
import random 

class Bloco(arcade.Sprite):
    def __init__(self, x: float, y: float):
        super().__init__("Jogo/bloco.png", scale = 0.2)
        self.center_x = x
        self.center_y = y

class Player(arcade.Sprite):
    def __init__(self):
        super().__init__("Jogo/player_direita.png", scale=0.02)

        self.textura_direita = arcade.load_texture("Jogo/player_direita.png")
        self.textura_esquerda = arcade.load_texture("Jogo/player_esquerda.png")

    def update(self, delta_time):
        self.center_x += self.change_x
        
        if self.change_x > 0:
            self.texture = self.textura_direita
        elif self.change_x < 0:
            self.texture = self.textura_esquerda

        if self.right > 800:
            self.change_x = 0
            self.right = 800
        if self.left < 0:
            self.change_x = 0
            self.left = 0

class Inimigo(arcade.Sprite):
    def __init__(self):
        super().__init__("Jogo/inimigo.png", scale = 1)

    def aplicar_efeito(self, jogo):
        jogo.pontuacao -= 1

    def update(self, delta_time):
            self.center_x += self.change_x
            self.center_y += self.change_y
    
            if self.right > 800 or self.left < 0:
                self.change_x *= -1
            if self.top > 600 or self.bottom < 0:
                self.change_y *= -1

class InimigoEspecial(arcade.Sprite):
    def __init__(self, jogo):
        super().__init__("Jogo/inimigo.png", scale=0.9)
        self.jogo = jogo

    def update(self, delta_time):
        jogador = self.jogo.jogador
        velocidade_inimigo = 1.5

        if jogador.center_x > self.center_x:
            self.change_x = velocidade_inimigo
        else:
            self.change_x = -velocidade_inimigo

        # if jogador.center_y > self.center_y:
        #     self.center_y += velocidade_inimigo
        # else:
        #     self.center_y -= velocidade_inimigo

    def aplicar_efeito(self, jogo):
        jogo.pontuacao -= 1
        self.center_x = random.randint(50, 750)
        self.center_y = 90

class Moeda(arcade.Sprite):
    def __init__(self):
        super().__init__("Jogo/estrela.png", scale = 1.5)

    def update(self, delta_time):
        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.right > 800 or self.left < 0:
            self.change_x = 0 
        if self.top > 600 or self.bottom < 0:
            self.change_y = 0 

class MoedaEspecial(arcade.Sprite):
    def __init__(self):
        super().__init__("Jogo/estrela.png", scale = 1.5)

    def update(self, delta_time):
        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.right > 800 or self.left < 0:
                self.change_x *= -1
        if self.top > 600 or self.bottom < 0:
                self.change_y *= -1

class InstrucoesView(arcade.View):
    def on_show_view(self):
        arcade.set_background_color((47, 16, 48))

    def on_draw(self):
        self.clear()

        arcade.draw_text("INSTRUÇÕES", 400, 450, arcade.color.WHITE, 30, anchor_x="center")

        arcade.draw_text("Use W A S D para mover o jogador", 400, 360, arcade.color.WHITE, 18, anchor_x="center")
        arcade.draw_text("Colete moedas para ganhar pontos", 400, 320, arcade.color.WHITE, 18, anchor_x="center")
        arcade.draw_text("Moeda especial vale +5 pontos", 400, 280, arcade.color.WHITE, 18, anchor_x="center")
        arcade.draw_text("Evite os inimigos (-1 ponto)", 400, 240, arcade.color.WHITE, 18, anchor_x="center")
        arcade.draw_text("O inimigo especial te persegue!", 400, 200, arcade.color.WHITE, 18, anchor_x="center")

        arcade.draw_text("Pressione M para voltar ao menu", 400, 120, arcade.color.WHITE, 16, anchor_x="center")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.M or key == arcade.key.ESCAPE:
            self.window.show_view(MenuView())

class SobreView(arcade.View):
    def __init__(self):
        super().__init__()
        self.autora_sprite = arcade.SpriteList()

        self.avatar = arcade.Sprite("Jogo/mica.png", scale=0.5) 
        self.avatar.center_x = 400
        self.avatar.center_y = 170
        self.autora_sprite.append(self.avatar)

    def on_show_view(self):
        arcade.set_background_color((47, 16, 48))

    def on_draw(self):
        self.clear()

        arcade.draw_text("SOBRE O JOGO", 400, 450, arcade.color.WHITE, 30, anchor_x="center")

        arcade.draw_text("Jogo desenvolvido com Python Arcade", 400, 350, arcade.color.WHITE, 18, anchor_x="center")
        arcade.draw_text("Exercício de Programação Orientada a Objetos", 400, 310, arcade.color.WHITE, 18, anchor_x="center")

        arcade.draw_text("Autora: Micaelly Victoria Peixoto de Oliveira", 400, 250, arcade.color.WHITE, 18, anchor_x="center")
        self.autora_sprite.draw()

        arcade.draw_text("Pressione M para voltar ao menu", 400, 80, arcade.color.WHITE, 16, anchor_x="center")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.M or key == arcade.key.ESCAPE:
            self.window.show_view(MenuView())

class MenuView(arcade.View):
    def __init__(self):
        super().__init__()

        self.fundo_menu = arcade.load_texture("Jogo/fundo_menu.png")

    def on_show_view(self):
        pass

    def on_draw(self):
        self.clear()

        arcade.draw_texture_rect(self.fundo_menu, arcade.XYWH(400, 300, 800, 600))

        arcade.draw_text("Cosmic Run", 400, 450, arcade.color.WHITE, 30, anchor_x="center")
        arcade.draw_text("[J] Jogar", 400, 320, arcade.color.WHITE, 20, anchor_x="center")
        arcade.draw_text("[I] Instruções", 400, 280, arcade.color.WHITE, 20, anchor_x="center")
        arcade.draw_text("[S] Sobre", 400, 240, arcade.color.WHITE, 20, anchor_x="center")
        arcade.draw_text("[ESC] Sair", 400, 200, arcade.color.WHITE, 20, anchor_x="center")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.J:
            self.window.show_view(JogoView())

        elif key == arcade.key.I:
            self.window.show_view(InstrucoesView())

        elif key == arcade.key.S:
            self.window.show_view(SobreView())

        elif key == arcade.key.ESCAPE:
            arcade.close_window()

class GameOverView(arcade.View):
    def __init__(self, pontuacao, tempo, pontuacao_maxima):
        super().__init__()
        self.pontuacao = pontuacao
        self.tempo = tempo
        self.pontuacao_maxima = pontuacao_maxima

        self.fundo_game_over = arcade.load_texture("Jogo/fundo_gameover.png")

    def on_draw(self):
        self.clear()

        arcade.draw_texture_rect(self.fundo_game_over, arcade.XYWH(400, 300, 800, 600))

        arcade.draw_text("FIM DE JOGO", 400, 480, arcade.color.YELLOW, 30, anchor_x="center")

        if self.pontuacao >= self.pontuacao_maxima:
            arcade.draw_text("EXCELENTE! PARABÉNS!", 400, 420, arcade.color.GREEN, 22, anchor_x="center")
            arcade.draw_text("Você escapou de todos os inimigos perfeitamente!", 400, 380, arcade.color.LIGHT_GREEN, 16, anchor_x="center")
        else:
            arcade.draw_text("PARABÉNS POR CONCLUIR!", 400, 420, arcade.color.WHITE, 20, anchor_x="center")

        arcade.draw_text(f"Pontuação Final: {self.pontuacao} / {self.pontuacao_maxima}", 400, 300, arcade.color.WHITE, 20, anchor_x="center")
        arcade.draw_text(f"Tempo Total: {self.tempo:.2f}s", 400, 260, arcade.color.WHITE, 20, anchor_x="center")

        arcade.draw_text("Pressione M para voltar ao Menu", 400, 180, arcade.color.GRAY, 16, anchor_x="center")
        arcade.draw_text("Pressione R para Jogar Novamente", 400, 140, arcade.color.GREEN, 16, anchor_x="center")
        arcade.draw_text("Pressione ESC para Sair", 400, 100, arcade.color.RED, 16, anchor_x="center")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            arcade.close_window() 

        elif key == arcade.key.R:
            self.window.show_view(JogoView())

        if key == arcade.key.M:
            self.window.show_view(MenuView())

class JogoView(arcade.View):
    def __init__(self):
        super().__init__()

        self.sprite_blocos = arcade.SpriteList()

        for x in range(32, 800 + 32, 64):
            chao = Bloco(x=x, y=30)
            self.sprite_blocos.append(chao)

        posicoes_plataforma = [(200, 250), (600, 250), (400, 450)]
        for x, y in posicoes_plataforma:
            plataforma = Bloco(x, y)
            self.sprite_blocos.append(plataforma)

        self.velocidade = 3

        self.fundo = arcade.load_texture("Jogo/fundo.png")

        self.setup()

    def setup(self):

        self.mensagem = ""
        self.tempo_mensagem = 0

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

        self.engine_fisica = arcade.PhysicsEnginePlatformer(
            player_sprite = self.jogador,
            walls = self.sprite_blocos,
            gravity_constant=0.5)

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
            moeda_simples = Moeda()

            posicao_valida = False
            while not posicao_valida:
                    moeda_simples.center_x = random.randint(50, 750)
                    moeda_simples.center_y = random.randint(100, 550)

                    if not arcade.check_for_collision_with_list(moeda_simples, self.sprite_blocos):
                        posicao_valida = True

            self.sprite_moeda.append(moeda_simples)

        self.inimigo_especial = InimigoEspecial(self)
        self.inimigo_especial.center_x = 400
        self.inimigo_especial.center_y = 300
        self.sprite_inimigos.append(self.inimigo_especial)

        self.engine_fisica_inimigo_especial = arcade.PhysicsEnginePlatformer(
                player_sprite = self.inimigo_especial,
                walls = self.sprite_blocos,
                gravity_constant=0.5)

        self.pontuacao_maxima = 25 + 1 + 5
        
    def on_draw(self):
        self.clear()

        arcade.draw_texture_rect(self.fundo, arcade.XYWH(400, 300, 800, 600))

        self.sprite_jogador.draw()
        self.sprite_moeda.draw()
        self.sprite_inimigos.draw()
        self.sprite_blocos.draw()

        arcade.draw_text(f"Tempo: {self.tempo:.2f}s", 10, 570, arcade.color.WHITE, 20)

        arcade.draw_text(f"Pontuação: {self.pontuacao}", 10, 540, arcade.color.WHITE, 20)

        if self.tempo_mensagem > 0:
            arcade.draw_text(self.mensagem, 400, 500, arcade.color.RED, 20, anchor_x="center")

    def on_update(self, delta_time):

        self.engine_fisica.update()
        self.engine_fisica_inimigo_especial.update()

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

                    self.mensagem = "Você foi atingido!"
                    self.tempo_mensagem = 1.5

            if len(self.sprite_moeda) == 0:
                game_over = GameOverView(self.pontuacao, self.tempo, self.pontuacao_maxima)
                self.window.show_view(game_over)

            if self.tempo_mensagem > 0:
                self.tempo_mensagem -= delta_time

    def on_key_press(self, key, modifiers):
        if key == arcade.key.A: 
            self.jogador.change_x = -self.velocidade
        elif key == arcade.key.D:
            self.jogador.change_x = self.velocidade

        if key == arcade.key.W or key == arcade.key.SPACE:
            if self.engine_fisica.can_jump():
                self.jogador.change_y = 16

        if key == arcade.key.R:
            self.setup()   

        if key == arcade.key.ESCAPE:
            self.window.show_view(MenuView())

    def on_key_release(self, key, modifiers):
        if key == arcade.key.A or key == arcade.key.D:
            self.jogador.change_x = 0
        elif key == arcade.key.W or key == arcade.key.S:
            self.jogador.change_y = 0

def main():
    tela = arcade.Window(800, 600, "Cosmic Run")

    menu = MenuView()
    tela.show_view(menu)

    arcade.run()

if __name__ == "__main__":
    main()