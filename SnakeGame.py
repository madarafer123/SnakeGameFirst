# Configurações Iniciais 
import pygame
import random
import time
import os
import sys

def resource_path(relative_path):
    """Obtem o caminho para o recurso, funciona para desenvolvimento e para o executável."""
    try:
        # PyInstaller cria uma pasta temporária e armazena os arquivos no diretório temporário
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

pygame.init()
pygame.display.set_caption("Classic Snake Game 90s (Python)")
largura = 1080
altura = 720
tela = pygame.display.set_mode((largura, altura))
relogio = pygame.time.Clock()

# Carregar o logo do jogo
logo = pygame.image.load(resource_path("Icon\Logo Cobrinha.png"))  # Substitua pelo caminho correto do arquivo
logo = pygame.transform.scale(logo, (200, 100))  # Redimensiona o logo

# Carregando sons
comer_macas_sound = pygame.mixer.Sound(resource_path("Efeitos sonoros\Comer.mp3"))  # Efeito sonoro para comer maçãs
game_over_sound = pygame.mixer.Sound(resource_path("Efeitos sonoros\GameOveryhhh.mp3"))  # Efeito sonoro de Game Over

# Música de fundo com volume reduzido
pygame.mixer.music.load(resource_path("Efeitos sonoros\Musicadefundo.mp3"))  
pygame.mixer.music.set_volume(0.01)  # Reduzindo o volume da música de fundo
pygame.mixer.music.play(-1)  # Toca a música de fundo em loop

# Cores RGB
preto = (0, 0, 0)
branco = (255, 255, 255)
vermelho = (255, 0, 0)
verde = (0, 255, 0)
azul = (0, 0, 255)  # Cor para maçãs especiais
violeta = (148,0,211)

# Parâmetros da cobra e jogo
tamanho_quadrado = 20
velocidade_jogo = 15
dificuldade = 0  # 0: Fácil, 1: Médio, 2: Difícil

def desenhar_vidas(vidas):
    fonte = pygame.font.SysFont("Times New Roman", 25)
    texto_vidas = fonte.render(f"Vidas: {vidas}", True, violeta)
    tela.blit(texto_vidas, [2, 30])  # Mostra as vidas na tela, abaixo do score

def criar_macas():
    macas_x = round(random.randrange(0, largura - tamanho_quadrado) / float(tamanho_quadrado)) * float(tamanho_quadrado)
    macas_y = round(random.randrange(0, altura - tamanho_quadrado) / float(tamanho_quadrado)) * float(tamanho_quadrado)
    return macas_x, macas_y

def criar_maca_especial():
    macas_x = round(random.randrange(0, largura - tamanho_quadrado) / float(tamanho_quadrado)) * float(tamanho_quadrado)
    macas_y = round(random.randrange(0, altura - tamanho_quadrado) / float(tamanho_quadrado)) * float(tamanho_quadrado)
    return macas_x, macas_y

def desenhar_macas(tamanho, macas_x, macas_y, especial=False):
    cor = azul if especial else vermelho
    pygame.draw.rect(tela, cor, [macas_x, macas_y, tamanho, tamanho])

def draw_snake(tamanho, pixels):
    for pixel in pixels:
        pygame.draw.rect(tela, branco, [pixel[0], pixel[1], tamanho, tamanho])

def draw_score(score):
    fonte = pygame.font.SysFont("Times New Roman", 25)
    texto = fonte.render(f"Score: {score}", True, verde)
    tela.blit(texto, [2, 2])

def select_speed(key):
    if key == pygame.K_DOWN:
        velocidade_x = 0
        velocidade_y = tamanho_quadrado
    elif key == pygame.K_UP:
        velocidade_x = 0
        velocidade_y = -tamanho_quadrado
    elif key == pygame.K_RIGHT:
        velocidade_x = tamanho_quadrado
        velocidade_y = 0  
    elif key == pygame.K_LEFT:
        velocidade_x = -tamanho_quadrado
        velocidade_y = 0
    return velocidade_x, velocidade_y

def definir_parametros_dificuldade(dificuldade):
    global tamanho_quadrado, velocidade_jogo
    if dificuldade == 0:  # Fácil
        tamanho_quadrado = 20
        velocidade_jogo = 10
    elif dificuldade == 1:  # Médio
        tamanho_quadrado = 15
        velocidade_jogo = 15
    elif dificuldade == 2:  # Difícil
        tamanho_quadrado = 10
        velocidade_jogo = 20

def correr_jogo():
    global dificuldade
    definir_parametros_dificuldade(dificuldade)

    game_over = False
    vidas = 3  # Adiciona o número de vidas

    x = largura / 2
    y = altura / 2

    velocidade_x = 0
    velocidade_y = 0

    tamanho_cobra = 1
    pixels = []

    macas_x, macas_y = criar_macas()
    maca_especial_x, maca_especial_y = None, None
    tempo_maca_especial = 0

    while not game_over:
        tela.fill(preto)

        # Mostrar as vidas na tela
        desenhar_vidas(vidas)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                game_over = True
            elif evento.type == pygame.KEYDOWN:
                velocidade_x, velocidade_y = select_speed(evento.key)

        # Desenhar Maçã Normal
        desenhar_macas(tamanho_quadrado, macas_x, macas_y)

        # Criar maçã especial a cada 10 maçãs normais
        if tamanho_cobra % 10 == 0 and maca_especial_x is None:
            maca_especial_x, maca_especial_y = criar_maca_especial()
            tempo_maca_especial = time.time()  # Armazena o tempo atual

        # Desenhar Maçã Especial, se existir
        if maca_especial_x is not None and time.time() - tempo_maca_especial < 5:  # A maçã especial aparece por 5 segundos
            desenhar_macas(tamanho_quadrado, maca_especial_x, maca_especial_y, especial=True)
        else:
            maca_especial_x, maca_especial_y = None, None  # Remove a maçã especial quando o tempo acabar

        # Atualizar a posição da cobra
        if x < 0 or x >= largura or y < 0 or y >= altura or [x, y] in pixels[:-1]:
            vidas -= 1  # Perde uma vida ao bater na parede ou em si mesmo
            if vidas > 0:
                # Resetar a cobra sem terminar o jogo
                x = largura / 2
                y = altura / 2
                velocidade_x = 0
                velocidade_y = 0
                tamanho_cobra = 1
                pixels = []
            else:
                # Se as vidas acabarem, game over
                game_over = True

        x += velocidade_x
        y += velocidade_y

        # Desenhar Cobra
        pixels.append([x, y])
        if len(pixels) > tamanho_cobra:
            del pixels[0]

        # se a cobra bateu no próprio corpo
        for pixel in pixels[:-1]:
            if pixel == [x, y]:
                vidas -= 1
                if vidas > 0:
                    # Resetar a cobra sem terminar o jogo
                    x = largura / 2
                    y = altura / 2
                    velocidade_x = 0
                    velocidade_y = 0
                    tamanho_cobra = 1
                    pixels = []
                else:
                    game_over = True

        draw_snake(tamanho_quadrado, pixels)

        # Pontuação
        draw_score(tamanho_cobra - 1)

        # Atualização de tela
        pygame.display.update()

        # Criar uma nova maçã
        if x == macas_x and y == macas_y:
            tamanho_cobra += 1
            macas_x, macas_y = criar_macas()
            comer_macas_sound.play()  # Toca o efeito sonoro ao comer maçã

        # Verificar se a cobra comeu a maçã especial
        if maca_especial_x is not None and x == maca_especial_x and y == maca_especial_y:
            tamanho_cobra += 3  # Aumenta mais agressivamente
            maca_especial_x, maca_especial_y = None, None  # Remove a maçã especial

        relogio.tick(velocidade_jogo)

    # Quando o jogo acaba, chamar a tela de game over
    pygame.mixer.music.stop()  # Parar a música de fundo no Game Over
    game_over_sound.play()  # Toca o efeito sonoro de game over
    tela_game_over(tamanho_cobra - 1)

def tela_game_over(score):
    game_over_ativo = True
    selecionado = 0  # 0 = Tentar Novamente, 1 = Voltar para o Menu Principal, 2 = Sair

    while game_over_ativo:
        tela.fill(preto)
        fonte_titulo = pygame.font.SysFont("Times New Roman", 60)
        fonte_opcao = pygame.font.SysFont("Times New Roman", 40)

        # Centralizando a mensagem de Game Over
        game_over_texto = fonte_titulo.render("Game Over", True, vermelho)
        game_over_rect = game_over_texto.get_rect(center=(largura // 2, altura // 4))
        tela.blit(game_over_texto, game_over_rect)

        # Mostrando a pontuação final
        pontuacao_final_texto = fonte_opcao.render(f"Sua Pontuação: {score}", True, branco)
        pontuacao_final_rect = pontuacao_final_texto.get_rect(center=(largura // 2, altura // 2 - 50))
        tela.blit(pontuacao_final_texto, pontuacao_final_rect)

        # Centralizando as opções
        if selecionado == 0:
            tentar_novamente_texto = fonte_opcao.render("> Tentar Novamente <", True, branco)
            voltar_menu_texto = fonte_opcao.render("Voltar para o Menu Principal", True, branco)
            sair_texto = fonte_opcao.render("Sair", True, branco)
        elif selecionado == 1:
            tentar_novamente_texto = fonte_opcao.render("Tentar Novamente", True, branco)
            voltar_menu_texto = fonte_opcao.render("> Voltar para o Menu Principal <", True, branco)
            sair_texto = fonte_opcao.render("Sair", True, branco)
        else:
            tentar_novamente_texto = fonte_opcao.render("Tentar Novamente", True, branco)
            voltar_menu_texto = fonte_opcao.render("Voltar para o Menu Principal", True, branco)
            sair_texto = fonte_opcao.render("> Sair <", True, branco)

        tentar_novamente_rect = tentar_novamente_texto.get_rect(center=(largura // 2, altura // 2))
        voltar_menu_rect = voltar_menu_texto.get_rect(center=(largura // 2, altura // 2 + 50))
        sair_rect = sair_texto.get_rect(center=(largura // 2, altura // 2 + 100))

        tela.blit(tentar_novamente_texto, tentar_novamente_rect)
        tela.blit(voltar_menu_texto, voltar_menu_rect)
        tela.blit(sair_texto, sair_rect)

        pygame.display.update()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                game_over_ativo = False
                pygame.quit()
                quit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    selecionado = (selecionado - 1) % 3  # Alterna entre 0, 1 e 2
                elif evento.key == pygame.K_DOWN:
                    selecionado = (selecionado + 1) % 3  # Alterna entre 0, 1 e 2
                elif evento.key == pygame.K_RETURN:  # Pressionou ENTER
                    if selecionado == 0:
                        correr_jogo()
                    elif selecionado == 1:
                        pygame.mixer.music.play(-1)  # Voltar a tocar a música de fundo ao voltar para o menu
                        menu_principal()  # Chama a função para voltar ao menu principal
                    else:
                        game_over_ativo = False
                        pygame.quit()
                        quit()

def tela_regras():
    regras_ativo = True
    while regras_ativo:
        tela.fill(preto)
        fonte = pygame.font.SysFont("Times New Roman", 40)
        
        # Adicione as regras do jogo aqui
        regras_texto = [
            "Regras do Jogo:",
            "1. Use as setas para mover a cobra.",
            "2. Coma as maçãs para crescer.",
            "3. Evite bater nas paredes e em si mesmo.",
            "4. A maçã azul é especial e dá mais pontos!",
            "5. Você pode escolher a dificuldade no menu.",
            "Pressione 'V' para voltar ao menu principal.",
        ]
        
        for i, linha in enumerate(regras_texto):
            texto_renderizado = fonte.render(linha, True, branco)
            tela.blit(texto_renderizado, (50, 50 + i * 40))

        pygame.display.update()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                regras_ativo = False
                pygame.quit()
                quit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_v:
                    regras_ativo = False

def menu_principal():
    global dificuldade
    menu_ativo = True
    selecionado = 0  # 0 = Jogar, 1 = Dificuldade, 2 = Regras, 3 = Sair

    while menu_ativo:
        tela.fill(preto)
        fonte = pygame.font.SysFont("Times New Roman", 60)
        fonte_opcao = pygame.font.SysFont("Times New Roman", 40)

        # Desenha o logo do jogo
        tela.blit(logo, (largura // 2 - 100, altura // 4))  # Centraliza o logo na parte superior

        # Centralizando o título
        titulo_texto = fonte.render("Classic Snake Game 90s", True, verde)
        titulo_rect = titulo_texto.get_rect(center=(largura // 2, altura // 6))
        tela.blit(titulo_texto, titulo_rect)

        # Centralizando as opções
        opcoes = ["Jogar", "Dificuldade", "Regras", "Sair"]
        for i, opcao in enumerate(opcoes):
            if selecionado == i:
                texto_renderizado = fonte_opcao.render(f"> {opcao} <", True, branco)
            else:
                texto_renderizado = fonte_opcao.render(opcao, True, branco)
            opcao_rect = texto_renderizado.get_rect(center=(largura // 2, altura // 2 + i * 60))
            tela.blit(texto_renderizado, opcao_rect)

        pygame.display.update()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                menu_ativo = False
                pygame.quit()
                quit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    selecionado = (selecionado - 1) % 4  # Alterna entre 0, 1, 2 e 3
                elif evento.key == pygame.K_DOWN:
                    selecionado = (selecionado + 1) % 4  # Alterna entre 0, 1, 2 e 3
                elif evento.key == pygame.K_RETURN:  # Pressionou ENTER
                    if selecionado == 0:
                        correr_jogo()
                    elif selecionado == 1:
                        selecionar_dificuldade()  # Chama a função de seleção de dificuldade
                    elif selecionado == 2:
                        tela_regras()  # Chama a função de regras
                    else:
                        menu_ativo = False
                        pygame.quit()
                        quit()

def selecionar_dificuldade():
    global dificuldade
    dificuldade_ativo = True
    while dificuldade_ativo:
        tela.fill(preto)
        fonte = pygame.font.SysFont("Times New Roman", 40)

        # Título da tela de dificuldade
        dificuldade_texto = fonte.render("Escolha a Dificuldade", True, branco)
        dificuldade_rect = dificuldade_texto.get_rect(center=(largura // 2, altura // 4))
        tela.blit(dificuldade_texto, dificuldade_rect)

        # Opções de dificuldade
        opcoes_dificuldade = ["Fácil", "Médio", "Difícil"]
        for i, opcao in enumerate(opcoes_dificuldade):
            if dificuldade == i:
                texto_renderizado = fonte.render(f"> {opcao} <", True, branco)
            else:
                texto_renderizado = fonte.render(opcao, True, branco)
            opcao_rect = texto_renderizado.get_rect(center=(largura // 2, altura // 2 + i * 60))
            tela.blit(texto_renderizado, opcao_rect)

        pygame.display.update()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                dificuldade_ativo = False
                pygame.quit()
                quit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    dificuldade = (dificuldade - 1) % 3  # Alterna entre 0, 1 e 2
                elif evento.key == pygame.K_DOWN:
                    dificuldade = (dificuldade + 1) % 3  # Alterna entre 0, 1 e 2
                elif evento.key == pygame.K_RETURN:  # Pressionou ENTER
                    dificuldade_ativo = False

# Inicia o jogo
menu_principal()
