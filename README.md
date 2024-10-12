# SnakeGameFirst

# Classic Snake Game 90s (Python)

Este repositório contém o código-fonte de um jogo da cobrinha clássico inspirado na versão dos anos 90, desenvolvido com Python e a biblioteca `pygame`.  
O jogo inclui diversos recursos, como diferentes níveis de dificuldade, vidas extras, maçãs especiais e efeitos sonoros nostálgicos!

## Funcionalidades Principais

- **Movimentação da Cobrinha**: Controlada pelas setas do teclado.
- **Maçãs Especiais**: Aparecem periodicamente e concedem mais pontos.
- **Dificuldade Ajustável**: Três níveis de dificuldade (Fácil, Médio, Difícil).
- **Vidas Extras**: O jogador possui até três vidas antes do fim de jogo.
- **Efeitos Sonoros e Música**: Sons nostálgicos de comer maçãs e efeito de "Game Over".
- **Tela de Game Over**: Com opções para reiniciar o jogo, voltar ao menu principal ou sair.

## Instruções de Jogo

- **Movimento**: Use as setas direcionais do teclado para mover a cobrinha.
- **Objetivo**: Comer as maçãs para crescer e aumentar a pontuação.
- **Atenção**: Evite bater nas paredes ou em si mesmo, ou você perderá vidas.
- **Maçãs Especiais**: As maçãs azuis concedem bônus, mas desaparecem após 5 segundos.
- **Dificuldades**: No menu principal, é possível selecionar entre três dificuldades.

## Recursos

- **Imagens e Sons**: O projeto utiliza imagens e sons que podem ser personalizados, localizados nas pastas `Icon` e `Efeitos sonoros`.
- **Logo**: O logo do jogo é carregado no menu principal e pode ser alterado substituindo o arquivo `Logo Cobrinha.png` na pasta `Icon`.

## Como Personalizar

- **Imagens**: Substitua os arquivos na pasta `Icon` para alterar a aparência do jogo.
- **Sons**: Para modificar os efeitos sonoros, substitua os arquivos na pasta `Efeitos sonoros`.

## Controles

- Setas direcionais: Movem a cobrinha.
- Enter: Seleciona as opções no menu.
- `V`: Retorna ao menu principal na tela de regras.

## Estrutura do Código

- **menu_principal()**: Gerencia a navegação no menu principal.
- **correr_jogo()**: Executa a lógica do jogo principal, incluindo movimentação, colisão e pontuação.
- **tela_game_over()**: Exibe a tela de "Game Over" com opções de reiniciar ou sair.
- **tela_regras()**: Exibe as regras do jogo.
- **selecionar_dificuldade()**: Permite escolher a dificuldade.

## Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests com melhorias ou novas funcionalidades.
