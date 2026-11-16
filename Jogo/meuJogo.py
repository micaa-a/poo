import arcade
import math 
import random
from pontuacao import Pontuacao
from pontuacao import inicializar_banco

ALTURA = 600
LARGURA = 800

NUM_MOEDAS = 25
NUM_INIMIGOS = 2

POSICAO_INICIAL_JOGADOR = (40, 100)
DISTANCIA_MINIMA_INICIO = 400

LARGURA_MAPA = 1400
ALTURA_MAPA = 787

FUNDO_LARGURA_FRAME = 1400
FUNDO_ALTURA_FRAME = 787

FUNDO_FRAMES = 14
FUNDO_COLUNAS = 14

TEMPO_INVENCIVEL = 1.5
TEMPO_FLASH = 0.3
TEMPO_TREMOR = 0.35
INTENSIDADE_TREMOR = 8

FUNDO_ARQUIVO = "Jogo/spritesheet_space.png" 
FUNDO_FRAMES = 14
FUNDO_COLUNAS = 14      
FUNDO_TEMPO_FRAME = 0.3

PLATAFORMAS = [
    (200, 250, 3), (700, 250, 3), (1150, 250, 3),
    (450, 450, 3), (1000, 450, 3),
    (250, 650, 3), (800, 650, 3),
]

class Explosao_inimigo(arcade.Sprite):
    def __init__(self, x: float, y: float, quadros: list, scale: float = 1.0):
        super().__init__(quadros[0], scale=scale)

        self.center_x = x
        self.center_y = y

        self.quadros = quadros
        self.quadro_atual = 0
        self.tempo_animacao = 0.0

    def update(self, delta_time: float = 1/60):
        self.tempo_animacao += delta_time

        if self.tempo_animacao >= 0.09:
            self.tempo_animacao = 0.0
            self.quadro_atual += 1

            if self.quadro_atual >= len(self.quadros):
                self.remove_from_sprite_lists()
                return

            self.texture = self.quadros[self.quadro_atual]

class TelaNomeView(arcade.View):
    def __init__(self, pontos_finais, tempo_final):
        super().__init__()
        self.pontos = pontos_finais
        self.tempo = tempo_final
        self.nome_jogador = ""

    def on_show_view(self):
        arcade.set_background_color((30, 15, 40))

    def on_draw(self):
        self.clear()

        arcade.draw_rect_filled(arcade.XYWH(400, 310, 600, 400), (20, 10, 30, 230))
        arcade.draw_rect_outline(arcade.XYWH(400, 310, 600, 400), arcade.color.CYAN, 2)

        arcade.draw_text("SALVAR PONTUAÇÃO", 400, 440, arcade.color.GOLD, 26, anchor_x="center")
        arcade.draw_text(f"Pontos: {self.pontos} | Tempo: {self.tempo:.1f}s", 400, 390, arcade.color.WHITE, 18, anchor_x="center")
        
        arcade.draw_text("Digite seu nome (máx. 15 caracteres):", 400, 310, arcade.color.LIGHT_BLUE, 15, anchor_x="center")

        arcade.draw_rect_filled(arcade.XYWH(400, 255, 360, 45), (10, 5, 20, 250))
        arcade.draw_rect_outline(arcade.XYWH(400, 255, 360, 45), arcade.color.PURPLE, 2)
        
        texto_exibicao = self.nome_jogador + "_"
        arcade.draw_text(texto_exibicao, 400, 242, arcade.color.YELLOW, 22, anchor_x="center")

        arcade.draw_text("Pressione ENTER para salvar ou BACKSPACE para apagar", 400, 120, arcade.color.GRAY, 13, anchor_x="center")

    def on_text(self, text):
        if len(self.nome_jogador) < 15:
            self.nome_jogador += text

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.BACKSPACE:
            self.nome_jogador = self.nome_jogador[:-1]
        elif symbol == arcade.key.ENTER and len(self.nome_jogador.strip()) > 0:
            Pontuacao.create(
                nome_jogador=self.nome_jogador,
                pontos=self.pontos,
                tempo_partida=self.tempo
            )
            self.window.show_view(TelaRanking())

class TelaRanking(arcade.View):
    def __init__(self):
        super().__init__()
        self.melhores = list(Pontuacao
                            .select()
                            .order_by(Pontuacao.pontos.desc())
                            .limit(10))

    def on_show_view(self):
        arcade.set_background_color((30, 15, 40))

    def on_draw(self):
        self.clear()

        arcade.draw_rect_filled(arcade.XYWH(400, 310, 650, 460), (20, 10, 30, 220))
        arcade.draw_rect_outline(arcade.XYWH(400, 310, 650, 460), arcade.color.GOLD, 2)

        arcade.draw_text("🏆 RANKING - TOP 10", 400, 500, arcade.color.GOLD, 26, anchor_x="center")
        
        if not self.melhores:
            arcade.draw_text("Nenhuma pontuação registrada ainda!", 400, 300, arcade.color.WHITE, 16, anchor_x="center")
        else:
            y_inicial = 440
            for i, p in enumerate(self.melhores, 1):
                texto = f"{i}º - {p.nome_jogador} : {p.pontos} pts ({p.tempo_partida:.1f}s)"
                arcade.draw_text(texto, 400, y_inicial, arcade.color.WHITE, 15, anchor_x="center")
                y_inicial -= 32

        arcade.draw_text("Pressione M para voltar ao Menu", 400, 65, arcade.color.CYAN, 14, anchor_x="center")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.M:
            self.window.show_view(MenuView())

class Bloco(arcade.Sprite):
    def __init__(self, x: float, y: float):
        super().__init__("Jogo/bloco.png", scale = 0.12)
        self.center_x = x
        self.center_y = y

        self.escala_base = 0.12
        self.forca_quique = 0.0

    def quicar(self):
        if self.forca_quique == 0:
            self.forca_quique = 1.0

    def update(self, delta_time: float = 1/60):
        super().update()
        
        if self.forca_quique > 0:
            self.forca_quique -= 8.0 * delta_time
            if self.forca_quique < 0:
                self.forca_quique = 0
            
            import math
            fator = math.sin(self.forca_quique * math.pi) * 0.05
            self.scale = self.escala_base + fator
        else:
            self.scale = self.escala_base

class Player(arcade.Sprite):
    def __init__(self):
        """ super().__init__("Jogo/player_direita.png", scale=0.02)

        self.textura_direita = arcade.load_texture("Jogo/player_direita.png")
        self.textura_esquerda = arcade.load_texture("Jogo/player_esquerda.png")"""

        sheet_direita = arcade.load_spritesheet("Jogo/spritesheet.png")

        quadros_direita = sheet_direita.get_texture_grid(
            size = (139, 164),
            columns = 6,
            count = 6
        )

        quadros_esquerda = []

        for frame in quadros_direita:
            quadros_esquerda.append(frame.flip_left_right())

        super().__init__(quadros_direita[0], scale = 0.5)

        self.textura_parado_d = quadros_direita[0]
        self.textura_parado_e = quadros_esquerda[0]

        self.passos_direita = [quadros_direita[1], quadros_direita[2], quadros_direita[3], quadros_direita[4]]
        self.passos_esquerda = [quadros_esquerda[1], quadros_esquerda[2], quadros_esquerda[3], quadros_esquerda[4]]

        self.textura_pulo_d = quadros_direita[5]
        self.textura_pulo_e = quadros_esquerda[5]
        self.textura_queda_d = quadros_direita[5]
        self.textura_queda_e = quadros_esquerda[5]

        self.quadro_atual: int = 0
        self.tempo_animacao: float = 0.0
        self.virado_para: str = "DIREITA" 

    def update(self, delta_time: float = 1/60):
        """self.center_x += self.change_x
        
        if self.change_x > 0:
            self.texture = self.textura_direita
        elif self.change_x < 0:
            self.texture = self.textura_esquerda

        if self.right > 800:
            self.change_x = 0
            self.right = 800
        if self.left < 0:
            self.change_x = 0
            self.left = 0"""

        if self.change_x > 0:
            self.virado_para = "DIREITA"
        elif self.change_x < 0:
            self.virado_para = "ESQUERDA"

        if self.change_y > 0:
            self.texture = self.textura_pulo_d if self.virado_para == "DIREITA" else self.textura_pulo_e
            return
        elif self.change_y < 0:
            self.texture = self.textura_queda_d if self.virado_para == "DIREITA" else self.textura_queda_e
            return

        if self.change_x == 0:
            self.texture = self.textura_parado_d if self.virado_para == "DIREITA" else self.textura_parado_e
            return
        
        self.tempo_animacao += delta_time
        if self.tempo_animacao >= 0.1:
            self.tempo_animacao = 0.0 
            self.quadro_atual = (self.quadro_atual + 1) % len(self.passos_direita)

            if self.virado_para == "DIREITA":
                self.texture = self.passos_direita[self.quadro_atual]
            else:
                self.texture = self.passos_esquerda[self.quadro_atual]

class Inimigo(arcade.Sprite):
    def __init__(self):
        sheet = arcade.load_spritesheet("Jogo/spritesheet_inimigo.png")
        self.quadros_direita = list(sheet.get_texture_grid(
            size=(334, 264), 
            columns=6,
            count=6
        ))

        self.quadros_esquerda = [frame.flip_left_right() for frame in self.quadros_direita]

        super().__init__(self.quadros_direita[0], scale=0.4)

        self.quadro_atual = 0
        self.tempo_animacao = 0.0

    def aplicar_efeito(self, jogo):
        jogo.pontuacao -= 1

    def update(self, delta_time: float = 1/60):
        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.right > LARGURA_MAPA or self.left < 0:
            self.change_x *= -1
        if self.top > ALTURA_MAPA or self.bottom < 0:
            self.change_y *= -1

        self.tempo_animacao += delta_time
        if self.tempo_animacao >= 0.1:  # Velocidade do bater de asas (menor = mais rápido)
            self.tempo_animacao = 0.0
            self.quadro_atual = (self.quadro_atual + 1) % len(self.quadros_direita)

            if self.change_x >= 0:
                self.texture = self.quadros_direita[self.quadro_atual]
            else:
                self.texture = self.quadros_esquerda[self.quadro_atual]

class InimigoEspecial(arcade.Sprite):
    def __init__(self, jogo):

        sheet_inimigo = arcade.load_spritesheet("Jogo/spritesheet_inimigo_especial.png")
        quadros_inimigo = list(sheet_inimigo.get_texture_grid(
            size = (234, 365), 
            columns = 4,
            count = 4
        ))

        quadros_inimigo_esquerda = []
        for frame in quadros_inimigo:
            quadros_inimigo_esquerda.append(frame.flip_left_right())

        super().__init__(quadros_inimigo[0], scale=0.3)
        self.jogo = jogo

        self.passos_direita = quadros_inimigo
        self.passos_esquerda = quadros_inimigo_esquerda
        
        self.quadro_atual = 0
        self.tempo_animacao = 0.0
        self.virado_para = "DIREITA"
        
    def update(self, delta_time):
        jogador = self.jogo.jogador
        velocidade_inimigo = 1.5

        if jogador.center_x > self.center_x:
            self.change_x = velocidade_inimigo
            self.virado_para = "DIREITA"
        else:
            self.change_x = -velocidade_inimigo
            self.virado_para = "ESQUERDA"

        if self.change_x != 0:
            self.tempo_animacao += delta_time
            if self.tempo_animacao >= 0.15:
                self.tempo_animacao = 0.0
                self.quadro_atual = (self.quadro_atual + 1) % len(self.passos_direita)
                
                if self.virado_para == "DIREITA":
                    self.texture = self.passos_direita[self.quadro_atual]
                else:
                    self.texture = self.passos_esquerda[self.quadro_atual]

    def aplicar_efeito(self, jogo):
        jogo.pontuacao -= 1
        for _ in range(100):
            x = random.randint(50, LARGURA_MAPA - 50)
            if abs(x - jogo.jogador.center_x) > 400:
                break
        self.center_x = x
        self.center_y = 90

class CoracaoVida(arcade.Sprite):
        def __init__(self, x: float, y: float):
            sheet = arcade.load_spritesheet("Jogo/spritesheet_coracao.png") 
            
            self.quadros = list(sheet.get_texture_grid(
                size=(45, 51),  
                columns=16,
                count=16
            ))
            
            super().__init__(self.quadros[0], scale=0.8)
            self.center_x = x
            self.center_y = y
            self.quadro_atual = 0.0

        def update(self, delta_time):
            self.quadro_atual += 8 * delta_time
            indice = int(self.quadro_atual) % 8
            self.texture = self.quadros[indice]

class CoracaoSumindo(arcade.Sprite):
    def __init__(self, x: float, y: float, quadros_totais: list):

        super().__init__(quadros_totais[8], scale=0.8)
        self.center_x = x
        self.center_y = y
        self.quadros = quadros_totais
        self.quadro_atual = 8.0 
        self.tempo_animacao = 0.0

    def update(self, delta_time: float = 1/60):
        self.tempo_animacao += delta_time
        if self.tempo_animacao >= 0.1:  
            self.tempo_animacao = 0.0
            self.quadro_atual += 1

            if self.quadro_atual >= len(self.quadros) or self.quadro_atual > 15:
                self.remove_from_sprite_lists()
                return

            self.texture = self.quadros[int(self.quadro_atual)]

class Moeda(arcade.Sprite):
    def __init__(self):
        sheet = arcade.load_spritesheet("Jogo/spritesheet_estrela.png")

        self.quadros = list(sheet.get_texture_grid(
            size=(126, 121),
            columns=8,
            count=8
        ))

        super().__init__(self.quadros[0], scale=0.5)
        self.quadro_atual = 0.0

    def update(self, delta_time):
        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.right > LARGURA_MAPA or self.left < 0:
            self.change_x = 0 
        if self.top > ALTURA_MAPA or self.bottom < 0:
            self.change_y = 0 

        self.quadro_atual += 6 * delta_time
        indice = int(self.quadro_atual) % 4
        self.texture = self.quadros[indice]

class MoedaEspecial(arcade.Sprite):
    def __init__(self):
        sheet = arcade.load_spritesheet("Jogo/spritesheet_estrela.png")

        self.quadros = list(sheet.get_texture_grid(
                    size=(126, 121),
                    columns=8,
                    count=8
                ))
        
        super().__init__(self.quadros[0], scale=0.5)
        self.quadro_atual = 0.0

    def update(self, delta_time):
        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.right > LARGURA_MAPA or self.left < 0:
                self.change_x *= -1
        if self.top > ALTURA_MAPA or self.bottom < 0:
                self.change_y *= -1

        self.quadro_atual += 6 * delta_time
        indice = int(self.quadro_atual) % 4
        self.texture = self.quadros[indice]

class ExplosaoMoeda(arcade.Sprite):
    def __init__(self, x: float, y: float, quadros_totais: list):
        super().__init__(quadros_totais[4], scale=0.5)
        self.center_x = x
        self.center_y = y
        self.quadros = quadros_totais
        self.quadro_atual = 4.0 
        self.tempo_animacao = 0.0

    def update(self, delta_time: float = 1/60):
        self.tempo_animacao += delta_time
        if self.tempo_animacao >= 0.15:
            self.tempo_animacao = 0.0
            self.quadro_atual += 1

            if self.quadro_atual >= len(self.quadros):
                self.remove_from_sprite_lists()
                return

            self.texture = self.quadros[int(self.quadro_atual)]

class InstrucoesView(arcade.View):
    def on_show_view(self):
        arcade.set_background_color((30, 15, 40))

    def on_draw(self):
        self.clear()

        arcade.draw_rect_filled(arcade.XYWH(400, 310, 600, 420), (20, 10, 30, 220))
        arcade.draw_rect_outline(arcade.XYWH(400, 310, 600, 420), arcade.color.CYAN, 2)

        arcade.draw_text("INSTRUÇÕES", 400, 470, arcade.color.GOLD, 28, anchor_x="center")

        comandos = [
            "Use W A S D para mover o jogador",
            "Colete moedas para ganhar pontos",
            "Moeda especial vale +5 pontos",
            "Evite os inimigos (-1 ponto e perde vida)",
            "O inimigo especial te persegue ativamente!"
        ]

        y = 410
        for texto in comandos:
            arcade.draw_text(f"• {texto}", 140, y, arcade.color.WHITE, 16)
            y -= 35

        arcade.draw_text("Pressione M ou ESC para voltar ao menu", 400, 120, arcade.color.CYAN, 14, anchor_x="center")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.M or key == arcade.key.ESCAPE:
            self.window.show_view(MenuView())

class SobreView(arcade.View):
    def __init__(self):
        super().__init__()
        self.autora_sprite = arcade.SpriteList()
        self.avatar = arcade.Sprite("Jogo/mica.png", scale=0.5) 
        self.avatar.center_x = 400
        self.avatar.center_y = 180
        self.autora_sprite.append(self.avatar)

    def on_show_view(self):
        arcade.set_background_color((30, 15, 40))

    def on_draw(self):
        self.clear()

        arcade.draw_rect_filled(arcade.XYWH(400, 320, 600, 440), (20, 10, 30, 220))
        arcade.draw_rect_outline(arcade.XYWH(400, 320, 600, 440), arcade.color.CYAN, 2)

        arcade.draw_text("SOBRE O JOGO", 400, 490, arcade.color.GOLD, 28, anchor_x="center")

        arcade.draw_text("Jogo desenvolvido com Python Arcade", 400, 410, arcade.color.WHITE, 16, anchor_x="center")
        arcade.draw_text("Exercício de Programação Orientada a Objetos", 400, 370, arcade.color.WHITE, 16, anchor_x="center")
        arcade.draw_text("Autora: Micaelly Victoria Peixoto de Oliveira", 400, 320, arcade.color.LIGHT_GREEN, 16, anchor_x="center")

        self.autora_sprite.draw()

        arcade.draw_text("Pressione M ou ESC para voltar ao menu", 400, 80, arcade.color.CYAN, 14, anchor_x="center")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.M or key == arcade.key.ESCAPE:
            self.window.show_view(MenuView())

class MenuView(arcade.View):
    def __init__(self):
        super().__init__()

        self.fundo_menu = arcade.load_texture("Jogo/fundo_menu.png")
        self.logo_titulo = arcade.load_texture("Jogo/logo_titulo.png")

        self.opcoes = [
            ("[J] Jogar", lambda: self.window.show_view(JogoView())),
            ("[R] Ver Ranking", lambda: self.window.show_view(TelaRanking())),
            ("[I] Instruções", lambda: self.window.show_view(InstrucoesView())),
            ("[S] Sobre", lambda: self.window.show_view(SobreView())),
            ("[ESC] Sair", lambda: arcade.close_window())
        ]
        self.selecionado = 0
        self.tempo_clique = 0.0

    def on_show_view(self):
        pass

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(self.fundo_menu, arcade.XYWH(400, 300, 800, 600))

        altura_logo = 250
    
        proporcao = self.logo_titulo.width / self.logo_titulo.height
        largura_logo = altura_logo * proporcao

        arcade.draw_texture_rect(
            self.logo_titulo, 
            arcade.XYWH(400, 480, largura_logo, altura_logo)
        )

        y_inicial = 350
        for i, (texto, acao) in enumerate(self.opcoes):
            is_selecionado = (i == self.selecionado)
            
            cor_fundo = (40, 25, 70, 240) if is_selecionado else (20, 10, 35, 180)
            cor_borda = arcade.color.CYAN if is_selecionado else arcade.color.PURPLE
            largura_box = 280 if is_selecionado else 260
            altura_box = 45 if is_selecionado else 40

            arcade.draw_rect_filled(arcade.XYWH(400, y_inicial, largura_box, altura_box), cor_fundo)
            arcade.draw_rect_outline(arcade.XYWH(400, y_inicial, largura_box, altura_box), cor_borda, 2 if is_selecionado else 1)
            
            cor_texto = arcade.color.YELLOW if is_selecionado else arcade.color.WHITE
            arcade.draw_text(texto, 400, y_inicial - 8, cor_texto, 18 if is_selecionado else 16, anchor_x="center")

            y_inicial -= 55

        arcade.draw_text("Use SETAS para navegar e ENTER para selecionar", 400, 40, arcade.color.GRAY, 13, anchor_x="center")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.W:
            self.selecionado = (self.selecionado - 1) % len(self.opcoes)
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.selecionado = (self.selecionado + 1) % len(self.opcoes)
        elif key == arcade.key.ENTER or key == arcade.key.SPACE:
            # Executa a ação da opção selecionada
            self.opcoes[self.selecionado][1]()
        elif key == arcade.key.J:
            self.window.show_view(JogoView())
        elif key == arcade.key.R:
            self.window.show_view(TelaRanking())
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
        
        # Opções do menu de Game Over para navegação com setas e ENTER (igual ao menu principal)
        self.opcoes = [
            ("Jogar Novamente [R]", lambda: self.window.show_view(JogoView())),
            ("Salvar e Ver Ranking [K]", lambda: self.window.show_view(TelaNomeView(self.pontuacao, self.tempo))),
            ("Voltar ao Menu [M]", lambda: self.window.show_view(MenuView())),
            ("Sair [ESC]", lambda: arcade.close_window())
        ]
        self.selecionado = 0

    def on_show_view(self):
        arcade.set_background_color((30, 15, 40))

    def on_draw(self):
        self.clear()

        arcade.draw_texture_rect(self.fundo_game_over, arcade.XYWH(400, 300, 800, 600))

        arcade.draw_rect_filled(arcade.XYWH(400, 310, 600, 440), (20, 10, 30, 230))
        arcade.draw_rect_outline(arcade.XYWH(400, 310, 600, 440), arcade.color.RED_DEVIL, 2)

        arcade.draw_text("FIM DE JOGO", 400, 475, arcade.color.YELLOW, 28, anchor_x="center")

        if self.pontuacao >= self.pontuacao_maxima:
            arcade.draw_text("EXCELENTE! PARABÉNS!", 400, 430, arcade.color.GREEN, 18, anchor_x="center")
            arcade.draw_text("Você escapou de todos os inimigos perfeitamente!", 400, 405, arcade.color.LIGHT_GREEN, 13, anchor_x="center")
        else:
            arcade.draw_text("PARABÉNS POR CONCLUIR!", 400, 420, arcade.color.WHITE, 16, anchor_x="center")

        arcade.draw_text(f"Pontuação Final: {self.pontuacao} / {self.pontuacao_maxima}", 400, 360, arcade.color.WHITE, 16, anchor_x="center")
        arcade.draw_text(f"Tempo Total: {self.tempo:.2f}s", 400, 325, arcade.color.CYAN, 16, anchor_x="center")

        y_inicial = 260
        for i, (texto, acao) in enumerate(self.opcoes):
            is_selecionado = (i == self.selecionado)
            
            cor_fundo = (50, 20, 30, 240) if is_selecionado else (25, 10, 20, 180)
            cor_borda = arcade.color.YELLOW if is_selecionado else arcade.color.DARK_RED
            largura_box = 320 if is_selecionado else 300
            altura_box = 36 if is_selecionado else 32

            arcade.draw_rect_filled(arcade.XYWH(400, y_inicial, largura_box, altura_box), cor_fundo)
            arcade.draw_rect_outline(arcade.XYWH(400, y_inicial, largura_box, altura_box), cor_borda, 2 if is_selecionado else 1)
            
            cor_texto = arcade.color.YELLOW if is_selecionado else arcade.color.WHITE
            arcade.draw_text(texto, 400, y_inicial - 6, cor_texto, 15 if is_selecionado else 14, anchor_x="center")

            y_inicial -= 45

        arcade.draw_text("Use SETAS para navegar e ENTER para selecionar (ou use as teclas de atalho)", 400, 50, arcade.color.GRAY, 12, anchor_x="center")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.W:
            self.selecionado = (self.selecionado - 1) % len(self.opcoes)
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.selecionado = (self.selecionado + 1) % len(self.opcoes)
        elif key == arcade.key.ENTER or key == arcade.key.SPACE:
            self.opcoes[self.selecionado][1]()
        elif key == arcade.key.ESCAPE:
            arcade.close_window() 
        elif key == arcade.key.R:
            self.window.show_view(JogoView())
        elif key == arcade.key.M:
            self.window.show_view(MenuView())
        elif key == arcade.key.K:
            self.window.show_view(TelaNomeView(self.pontuacao, self.tempo))

class JogoView(arcade.View):
    def __init__(self):
        super().__init__()

        self.camera = arcade.Camera2D()

        self.tempo_invencivel = 0.0
        self.tempo_flash = 0.0
        self.tempo_tremor = 0.0

        sheet_explosao = arcade.load_spritesheet("Jogo/spritesheet_explosao.png")
        self.quadros_explosao = sheet_explosao.get_texture_grid(
            size=(94, 94),
            columns=12,     
            count=12      
        )

        self.sprite_blocos = arcade.SpriteList()

        for x in range(32, LARGURA_MAPA + 32, 64):
            chao = Bloco(x=x, y=30)
            self.sprite_blocos.append(chao)

        for x_inicial, y, quantidade in PLATAFORMAS:
            ultimo_x = x_inicial + (quantidade - 1) * 64
            if ultimo_x + 32 > LARGURA_MAPA or y + 100 > ALTURA_MAPA:
                continue
            for i in range(quantidade):
                plataforma = Bloco(x_inicial + i * 64, y)
                self.sprite_blocos.append(plataforma)

        self.velocidade = 3

        sheet_fundo = arcade.load_spritesheet(FUNDO_ARQUIVO)
        self.quadros_fundo = sheet_fundo.get_texture_grid(
            size=(LARGURA_MAPA, ALTURA_MAPA),
            columns=FUNDO_COLUNAS,
            count=FUNDO_FRAMES
        )
        self.quadro_fundo = 0
        self.tempo_fundo = 0.0

        self.setup()

        self.tecla_esquerda_pressionada = False
        self.tecla_direita_pressionada = False

    def setup(self):

        self.estava_no_ar = False

        self.mensagem = ""
        self.tempo_mensagem = 0

        self.tempo = 0
        self.jogo_finalizado = False
        self.pontuacao = 0 

        self.vidas = 3
        self.sprite_vidas = arcade.SpriteList()
        for i in range(self.vidas):
            coracao = CoracaoVida(x=640 + (i * 35), y=562)
            self.sprite_vidas.append(coracao)

        self.sprite_efeitos = arcade.SpriteList()
        self.sprite_efeitos_hud = arcade.SpriteList()

        self.jogador = Player()
        self.jogador.left = 0
        self.jogador.bottom = 0       

        self.sprite_jogador = arcade.SpriteList()
        self.sprite_jogador.append(self.jogador)

        self.sprite_inimigos = arcade.SpriteList()
        for i in range(NUM_INIMIGOS):
            inimigo = Inimigo()
            self.posicionar_aleatoriamente(inimigo, 300, LARGURA_MAPA - 150, 150, ALTURA_MAPA - 150)
            inimigo.change_x = random.choice([-1, 1]) * self.velocidade
            inimigo.change_y = random.choice([-1, 1]) * (self.velocidade - 1)
            self.sprite_inimigos.append(inimigo)

        self.engine_fisica = arcade.PhysicsEnginePlatformer(
            player_sprite = self.jogador,
            walls = self.sprite_blocos,
            gravity_constant=0.5)

        self.sprite_moeda = arcade.SpriteList()

        self.moeda_especial = MoedaEspecial()
        self.posicionar_moeda(self.moeda_especial)
        self.moeda_especial.change_x = random.choice([-1, 1]) * self.velocidade
        self.moeda_especial.change_y = random.choice([-1, 1]) * (self.velocidade - 1)
        self.sprite_moeda.append(self.moeda_especial)

        for i in range(NUM_MOEDAS):
            moeda_simples = Moeda()
            self.posicionar_moeda(moeda_simples)
            self.sprite_moeda.append(moeda_simples)

        self.inimigo_especial = InimigoEspecial(self)
        self.posicionar_aleatoriamente(self.inimigo_especial, LARGURA_MAPA // 3, LARGURA_MAPA - 100, 150, 150)
        self.sprite_inimigos.append(self.inimigo_especial)

        self.engine_fisica_inimigo_especial = arcade.PhysicsEnginePlatformer(
                player_sprite = self.inimigo_especial,
                walls = self.sprite_blocos,
                gravity_constant=0.5)

        self.pontuacao_maxima = NUM_MOEDAS + 5

    def posicionar_aleatoriamente(self, sprite, x_min, x_max, y_min, y_max):
        for _ in range(300):
            sprite.center_x = random.randint(x_min, x_max)
            sprite.center_y = random.randint(y_min, y_max)

            distancia = math.hypot(
                sprite.center_x - POSICAO_INICIAL_JOGADOR[0],
                sprite.center_y - POSICAO_INICIAL_JOGADOR[1],
            )
            if distancia >= DISTANCIA_MINIMA_INICIO and not arcade.check_for_collision_with_list(sprite, self.sprite_blocos):
                return

    def posicionar_moeda(self, moeda):
        blocos = list(self.sprite_blocos)
        for _ in range(300):
            bloco = random.choice(blocos)
            moeda.center_x = max(50, min(LARGURA_MAPA - 50, bloco.center_x + random.randint(-30, 30)))
            moeda.center_y = bloco.top + random.randint(40, 180)

            if moeda.center_y > ALTURA_MAPA - 60:
                continue
            if not arcade.check_for_collision_with_list(moeda, self.sprite_blocos):
                return

    def on_draw(self):
        self.clear()

        self.camera.use()

        arcade.draw_texture_rect(
            texture=self.quadros_fundo[self.quadro_fundo],
            rect=arcade.XYWH(
                x=LARGURA_MAPA / 2,
                y=ALTURA_MAPA / 2,
                width=LARGURA_MAPA + 2 * INTENSIDADE_TREMOR,
                height=ALTURA_MAPA + 2 * INTENSIDADE_TREMOR
            )
        )

        self.sprite_jogador.draw()
        self.sprite_moeda.draw()
        self.sprite_inimigos.draw()
        self.sprite_blocos.draw()
        self.sprite_efeitos.draw()

        self.window.default_camera.use()

        arcade.draw_rect_filled(arcade.XYWH(400, 570, 800, 60), (15, 10, 25, 220))
        arcade.draw_line(0, 540, 800, 540, arcade.color.CYAN, 2)

        arcade.draw_text(f"⏱ TEMPO: {self.tempo:.1f}s", 20, 555, arcade.color.LIGHT_BLUE, 14)
        arcade.draw_text(f"⭐ PONTOS: {self.pontuacao} / {self.pontuacao_maxima}", 230, 555, arcade.color.GOLD, 16)
        arcade.draw_text("VIDAS:", 540, 555, arcade.color.RED, 14)
        self.sprite_vidas.draw()
        self.sprite_efeitos_hud.draw()

        if self.tempo_flash > 0:
            alpha = int(120 * self.tempo_flash / TEMPO_FLASH)
            arcade.draw_rect_filled(
                arcade.XYWH(LARGURA / 2, ALTURA / 2, LARGURA, ALTURA),
                (255, 0, 0, alpha)
            )
        
        if self.tempo_mensagem > 0:
            arcade.draw_text(self.mensagem, 400, 500, arcade.color.RED, 20, anchor_x="center")

    def on_update(self, delta_time):

        self.tempo_fundo += delta_time
        if self.tempo_fundo >= FUNDO_TEMPO_FRAME:
            self.tempo_fundo -= FUNDO_TEMPO_FRAME
            self.quadro_fundo = (self.quadro_fundo + 1) % FUNDO_FRAMES

        for bloco in self.sprite_blocos:
            bloco.update(delta_time)
    
        if self.tecla_esquerda_pressionada and not self.tecla_direita_pressionada:
            self.jogador.change_x = -self.velocidade
        elif self.tecla_direita_pressionada and not self.tecla_esquerda_pressionada:
            self.jogador.change_x = self.velocidade
        else:
            self.jogador.change_x = 0

        self.tempo_invencivel = max(0.0, self.tempo_invencivel - delta_time)
        self.tempo_flash = max(0.0, self.tempo_flash - delta_time)
        self.tempo_tremor = max(0.0, self.tempo_tremor - delta_time)

        cam_x = max(LARGURA / 2, min(self.jogador.center_x, LARGURA_MAPA - LARGURA / 2))
        cam_y = max(ALTURA / 2, min(self.jogador.center_y, ALTURA_MAPA - ALTURA / 2))

        if self.tempo_tremor > 0:
            forca = INTENSIDADE_TREMOR * self.tempo_tremor / TEMPO_TREMOR
            self.camera.position = (
                cam_x + random.uniform(-forca, forca),
                cam_y + random.uniform(-forca, forca),
            )
        else:
            self.camera.position = (cam_x, cam_y)

        if self.tempo_invencivel == 0:
            inimigos_colididos = arcade.check_for_collision_with_list(
                self.jogador, self.sprite_inimigos
            )
            if inimigos_colididos:
                self.tempo_invencivel = TEMPO_INVENCIVEL
                self.tempo_flash = TEMPO_FLASH
                self.tempo_tremor = TEMPO_TREMOR

                primeiro_inimigo = inimigos_colididos[0]

                x = (self.jogador.center_x + primeiro_inimigo.center_x) / 2
                y = (self.jogador.center_y + primeiro_inimigo.center_y) / 2

                explosao = Explosao_inimigo(x, y, self.quadros_explosao, scale=0.8)
                self.sprite_efeitos.append(explosao)

                for inimigo in inimigos_colididos:
                    inimigo.aplicar_efeito(self)

                self.vidas -= 1

                if len(self.sprite_vidas) > 0:
                    coracao_removido = self.sprite_vidas.pop()

                    efeito_sumico = CoracaoSumindo(coracao_removido.center_x, coracao_removido.center_y, coracao_removido.quadros)
                    self.sprite_efeitos_hud.append(efeito_sumico)

                if self.vidas <= 0:
                    game_over = GameOverView(self.pontuacao, self.tempo, self.pontuacao_maxima)
                    self.window.show_view(game_over)
                    return

        if self.tempo_invencivel > 0:
            if int(self.tempo_invencivel * 10) % 2 == 0:
                self.jogador.alpha = 80
            else:
                self.jogador.alpha = 255
        else:
            self.jogador.alpha = 255

        self.engine_fisica.update()
        self.engine_fisica_inimigo_especial.update()
            
        largura_meio_sprite = self.jogador.width / 2

        if self.jogador.left < 0:
            self.jogador.left = 0
            self.jogador.change_x = 0
        
        if self.jogador.right > LARGURA_MAPA:
            self.jogador.right = LARGURA_MAPA
            self.jogador.change_x = 0

        if not self.jogo_finalizado:
            self.tempo += delta_time

            self.sprite_vidas.update(delta_time)
            self.sprite_jogador.update(delta_time)
            self.sprite_moeda.update(delta_time)
            self.sprite_inimigos.update(delta_time)
            self.sprite_efeitos.update(delta_time)
            for efeito_hud in list(self.sprite_efeitos_hud):
                efeito_hud.update(delta_time)

            moedas_colididas = arcade.check_for_collision_with_list(self.jogador, self.sprite_moeda)
            for moeda in moedas_colididas:

                efeito_coleta = ExplosaoMoeda(moeda.center_x, moeda.center_y, moeda.quadros)
                self.sprite_efeitos.append(efeito_coleta)

                moeda.remove_from_sprite_lists()
                if moeda == self.moeda_especial:
                    self.pontuacao += 5
                else:
                    self.pontuacao += 1

            if len(self.sprite_moeda) == 0:
                game_over = GameOverView(self.pontuacao, self.tempo, self.pontuacao_maxima)
                self.window.show_view(game_over)

            if self.tempo_mensagem > 0:
                self.tempo_mensagem -= delta_time

    def on_key_press(self, key, modifiers):
        if key == arcade.key.A:
            self.tecla_esquerda_pressionada = True
        elif key == arcade.key.D:
            self.tecla_direita_pressionada = True

        if key == arcade.key.W or key == arcade.key.SPACE:
            if self.engine_fisica.can_jump():
                self.jogador.change_y = 16

        if key == arcade.key.R:
            self.setup()

        if key == arcade.key.ESCAPE:
            self.window.show_view(MenuView())

    def on_key_release(self, key, modifiers):
        if key == arcade.key.A:
            self.tecla_esquerda_pressionada = False
        elif key == arcade.key.D:
            self.tecla_direita_pressionada = False

def main():
    inicializar_banco()

    tela = arcade.Window(800, 600, "Cosmic Run")

    menu = MenuView()
    tela.show_view(menu)

    arcade.run()

if __name__ == "__main__":
    main()