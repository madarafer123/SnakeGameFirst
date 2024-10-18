# Initial Settings 
import pygame
import random
import time
import os
import sys

def resource_path(relative_path):
    """Gets the path to the resource, works for development and for the executable."""
    try:
        # PyInstaller creates a temporary folder and stores the files in the temporary directory
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

# Load the game logo
logo = pygame.image.load(resource_path("Icon\Logo Cobrinha.png"))  # Replace with the correct file path
logo = pygame.transform.scale(logo, (200, 100))  # Resize the logo

# Loading sounds
comer_macas_sound = pygame.mixer.Sound(resource_path("Efeitos sonoros\EatMaça1.mp3"))  # Sound effect for eating apples
game_over_sound = pygame.mixer.Sound(resource_path("Efeitos sonoros\GameOver.mp3"))  # Game Over sound effect
comer_macas_especial_sound = pygame.mixer.Sound(resource_path("Efeitos sonoros\EatMaça2.wav"))  # Sound for special apple

# Background music at reduced volume
pygame.mixer.music.load(resource_path("Efeitos sonoros\GameMusicFundo.mp3"))  
pygame.mixer.music.set_volume(0.05)  # Reducing the volume of the background music
pygame.mixer.music.play(-1)  # Play the background music on loop

# RGB colours
preto = (0, 0, 0)
branco = (255, 255, 255)
vermelho = (255, 0, 0)
verde = (0, 255, 0)
azul = (0, 0, 255)  # Colour for special apples
violeta = (148,0,211)

# Snake and game parameters
tamanho_quadrado = 20
velocidade_jogo = 15
dificuldade = 0  # 0: Easy, 1: Medium, 2: Difficult

def desenhar_vidas(vidas):
    fonte = pygame.font.SysFont("Times New Roman", 25)
    texto_vidas = fonte.render(f"Lives: {vidas}", True, violeta)
    tela.blit(texto_vidas, [2, 30])  # Shows the lives on the screen, below the score

def criar_macas():
    while True:
        macas_x = round(random.randrange(0, largura - tamanho_quadrado) / float(tamanho_quadrado)) * float(tamanho_quadrado)
        macas_y = round(random.randrange(50, altura - tamanho_quadrado) / float(tamanho_quadrado)) * float(tamanho_quadrado)
        # Prevent the apple from appearing in the Score and Lives area
        if macas_y >= 50: # Score and Lives occupy the top 50 pixels
            return macas_x, macas_y

def criar_maca_especial():
    while True:
        macas_x = round(random.randrange(0, largura - tamanho_quadrado) / float(tamanho_quadrado)) * float(tamanho_quadrado)
        macas_y = round(random.randrange(50, altura - tamanho_quadrado) / float(tamanho_quadrado)) * float(tamanho_quadrado)
        # Prevent the special apple from appearing in the Score and Lives area
        if macas_y >= 50:
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
    if dificuldade == 0:  # Easy
        tamanho_quadrado = 20
        velocidade_jogo = 10
    elif dificuldade == 1:  # Medium
        tamanho_quadrado = 15
        velocidade_jogo = 15
    elif dificuldade == 2:  # Difficult
        tamanho_quadrado = 10
        velocidade_jogo = 20

def correr_jogo():
    global dificuldade
    definir_parametros_dificuldade(dificuldade)

    game_over = False
    vidas = 3  # Add the number of lives

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

        # Show the lives on the screen
        desenhar_vidas(vidas)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                game_over = True
            elif evento.type == pygame.KEYDOWN:
                # Checks if the key pressed is a directional arrow
                if evento.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                    velocidade_x, velocidade_y = select_speed(evento.key)


        # Draw Normal Apple
        desenhar_macas(tamanho_quadrado, macas_x, macas_y)

        # Create a special apple for every 10 normal apples
        if tamanho_cobra % 10 == 0 and maca_especial_x is None:
            maca_especial_x, maca_especial_y = criar_maca_especial()
            tempo_maca_especial = time.time()  # Stores the current time

        # Draw Special Apple, if any
        if maca_especial_x is not None and time.time() - tempo_maca_especial < 5:  # The special apple appears for 5 seconds 
            desenhar_macas(tamanho_quadrado, maca_especial_x, maca_especial_y, especial=True)
        else:
            maca_especial_x, maca_especial_y = None, None  # Remove the special apple when the time is up

        # Update the snake's position
        if x < 0 or x >= largura or y < 0 or y >= altura or [x, y] in pixels[:-1]:
            vidas -= 1  # Lose a life by hitting the wall or yourself
            if vidas > 0:
                # Reset the snake without finishing the game
                x = largura / 2
                y = altura / 2
                velocidade_x = 0
                velocidade_y = 0
                tamanho_cobra = 1
                pixels = []
            else:
                # If lives run out, game over
                game_over = True

        x += velocidade_x
        y += velocidade_y

        # Draw Snake
        pixels.append([x, y])
        if len(pixels) > tamanho_cobra:
            del pixels[0]

        # if the snake hit its own body
        for pixel in pixels[:-1]:
            if pixel == [x, y]:
                vidas -= 1
                if vidas > 0:
                    # Reset the snake without finishing the game
                    x = largura / 2
                    y = altura / 2
                    velocidade_x = 0
                    velocidade_y = 0
                    tamanho_cobra = 1
                    pixels = []
                else:
                    game_over = True

        draw_snake(tamanho_quadrado, pixels)

        # Score
        draw_score(tamanho_cobra - 1)

        # Screen refresh
        pygame.display.update()

        # Create a new apple
        if x == macas_x and y == macas_y:
            tamanho_cobra += 1
            macas_x, macas_y = criar_macas()
            comer_macas_sound.play()  # Play the apple-eating sound effect

        # Check if the snake has eaten the special apple
        if maca_especial_x is not None and x == maca_especial_x and y == maca_especial_y:
            tamanho_cobra += 3  # Increase more aggressively
            maca_especial_x, maca_especial_y = None, None  # Remove the special apple
            comer_macas_especial_sound.play() # Play the sound of the special apple

        relogio.tick(velocidade_jogo)

    # When the game ends, call up the game over screen
    pygame.mixer.music.stop()  # Stop the background music in Game Over
    game_over_sound.play()  # Play the game over sound effect
    tela_game_over(tamanho_cobra - 1)

def tela_game_over(score):
    game_over_ativo = True
    selecionado = 0  # 0 = Try Again, 1 = Return to Main Menu, 2 = Exit

    while game_over_ativo:
        tela.fill(preto)
        fonte_titulo = pygame.font.SysFont("Times New Roman", 60)
        fonte_opcao = pygame.font.SysFont("Times New Roman", 40)

        # Centring the Game Over message
        game_over_texto = fonte_titulo.render("Game Over", True, vermelho)
        game_over_rect = game_over_texto.get_rect(center=(largura // 2, altura // 4))
        tela.blit(game_over_texto, game_over_rect)

        # Showing the final score
        pontuacao_final_texto = fonte_opcao.render(f"Your Score: {score}", True, branco)
        pontuacao_final_rect = pontuacao_final_texto.get_rect(center=(largura // 2, altura // 2 - 50))
        tela.blit(pontuacao_final_texto, pontuacao_final_rect)

        # Centralising the options
        if selecionado == 0:
            tentar_novamente_texto = fonte_opcao.render("> Try again <", True, branco)
            voltar_menu_texto = fonte_opcao.render("Back to Main Menu", True, branco)
            sair_texto = fonte_opcao.render("Exit", True, branco)
        elif selecionado == 1:
            tentar_novamente_texto = fonte_opcao.render("Try again", True, branco)
            voltar_menu_texto = fonte_opcao.render("> Back to Main Menu <", True, branco)
            sair_texto = fonte_opcao.render("Exit", True, branco)
        else:
            tentar_novamente_texto = fonte_opcao.render("Try again", True, branco)
            voltar_menu_texto = fonte_opcao.render("Back to Main Menu", True, branco)
            sair_texto = fonte_opcao.render("> Exit <", True, branco)

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
                    selecionado = (selecionado - 1) % 3  # Switches between 0, 1 and 2
                elif evento.key == pygame.K_DOWN:
                    selecionado = (selecionado + 1) % 3  # Switches between 0, 1 and 2
                elif evento.key == pygame.K_RETURN:  # Pressed ENTER
                    if selecionado == 0:
                        correr_jogo()
                    elif selecionado == 1:
                        pygame.mixer.music.play(-1)  # Play the background music again when you return to the menu
                        menu_principal()  # Calls the function to return to the main menu
                    else:
                        game_over_ativo = False
                        pygame.quit()
                        quit()

def tela_regras():
    regras_ativo = True
    while regras_ativo:
        tela.fill(preto)
        fonte = pygame.font.SysFont("Times New Roman", 40)
        
        # Add the game rules here
        regras_texto = [
            "Rules of the Game:",
            "1. Use the arrow keys to move the snake.",
            "2. Eat the apples to grow.",
            "3. Avoid hitting walls and yourself.",
            "4. The blue apple is special and gives you more points!",
            "5. You can choose the difficulty in the menu.",
            "Press 'V' to return to the main menu.",
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
    selecionado = 0  # 0 = Play, 1 = Difficulty, 2 = Rules, 3 = Exit

    while menu_ativo:
        tela.fill(preto)
        fonte = pygame.font.SysFont("Times New Roman", 60)
        fonte_opcao = pygame.font.SysFont("Times New Roman", 40)

        # Draw the game logo
        tela.blit(logo, (largura // 2 - 100, altura // 4))  # Centre the logo at the top

        # Centring the title
        titulo_texto = fonte.render("Classic Snake Game 90s", True, verde)
        titulo_rect = titulo_texto.get_rect(center=(largura // 2, altura // 6))
        tela.blit(titulo_texto, titulo_rect)

        # Centralising the options
        opcoes = ["Play", "Difficulty", "Rules", "Exit"]
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
                    selecionado = (selecionado - 1) % 4  # Switches between 0, 1, 2 and 3
                elif evento.key == pygame.K_DOWN:
                    selecionado = (selecionado + 1) % 4  # Switches between 0, 1, 2 and 3
                elif evento.key == pygame.K_RETURN:  # Pressed ENTER
                    if selecionado == 0:
                        correr_jogo()
                    elif selecionado == 1:
                        selecionar_dificuldade()  # Calls the difficulty selection function
                    elif selecionado == 2:
                        tela_regras()  # Call the rules function
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

        # Difficulty screen title
        dificuldade_texto = fonte.render("Choose the Difficulty", True, branco)
        dificuldade_rect = dificuldade_texto.get_rect(center=(largura // 2, altura // 4))
        tela.blit(dificuldade_texto, dificuldade_rect)

        # Difficulty options
        opcoes_dificuldade = ["Easy", "Medium", "Hard"]
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
                    dificuldade = (dificuldade - 1) % 3  # Switches between 0, 1 and 2
                elif evento.key == pygame.K_DOWN:
                    dificuldade = (dificuldade + 1) % 3  # Switches between 0, 1 and 2
                elif evento.key == pygame.K_RETURN:  # Pressed ENTER
                    dificuldade_ativo = False

# Start the game
menu_principal()
