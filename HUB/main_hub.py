## Autor: Vitor Augusto Tibério - Estudante de Engenharia Elétrica - USP São Carlos ## 

import pygame
import cv2
import mediapipe as mp
import sys

# Importando seus módulos de jogo
import jogo_sel_ninja
import jogo_osciloscopio
import jogo_lab_pdi

# Inicialização do Pygame e Hardware
pygame.init()
LARGURA, ALTURA = 1100, 700
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("ARCADE CENTER - SEL USP")

# Recursos Compartilhados
camera = cv2.VideoCapture(0)
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7)

# Cores do Tema (Neon)
COR_FUNDO = (22, 22, 35)
COR_TEXTO = (255, 255, 255)
COR_AMARELO = (255, 215, 0)
CORES_CARDS = [(255, 50, 50), (50, 150, 255), (50, 255, 150)] # Vermelho, Azul, Verde

# Fontes
fonte_titulo = pygame.font.SysFont("Impact", 80)
fonte_sub = pygame.font.SysFont("Consolas", 20)
fonte_card = pygame.font.SysFont("Impact", 35)

def desenhar_card(texto, subtexto, x, y, largura, altura, cor):
    mouse = pygame.mouse.get_pos()
    clique = pygame.mouse.get_pressed()
    
    # Efeito de Hover (brilho)
    rect = pygame.Rect(x, y, largura, altura)
    borda = 3
    if rect.collidepoint(mouse):
        borda = 6
        pygame.draw.rect(tela, cor, (x-5, y-5, largura+10, altura+10), border_radius=15, width=2)
        if clique[0] == 1:
            pygame.time.delay(200)
            return True

    # Desenho do Card
    pygame.draw.rect(tela, (30, 30, 45), rect, border_radius=15)
    pygame.draw.rect(tela, cor, rect, border_radius=15, width=borda)
    
    # Textos do Card
    txt_surf = fonte_card.render(texto, True, COR_TEXTO)
    sub_surf = fonte_sub.render(subtexto, True, (180, 180, 180))
    
    tela.blit(txt_surf, (x + (largura - txt_surf.get_width())//2, y + 80))
    tela.blit(sub_surf, (x + (largura - sub_surf.get_width())//2, y + 140))
    
    return False

def main():
    while True:
        tela.fill(COR_FUNDO)
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                camera.release()
                pygame.quit()
                sys.exit()

        # Título Principal
        titulo = fonte_titulo.render("JOGOS DE OPENCV", True, COR_AMARELO)
        tela.blit(titulo, (LARGURA//2 - titulo.get_width()//2, 60))
        
        chamada = fonte_sub.render("Escolha sua jogo:", True, COR_TEXTO)
        tela.blit(chamada, (LARGURA//2 - chamada.get_width()//2, 160))

        # Cards de Jogos (Layout em colunas como na imagem)
        larg_card, alt_card = 300, 220
        espacamento = 40
        x_inicial = (LARGURA - (3 * larg_card + 2 * espacamento)) // 2
        y_pos = 280

        # Card 1: SEL Ninja
        if desenhar_card("SEL NINJA", "Capture os componentes!", x_inicial, y_pos, larg_card, alt_card, CORES_CARDS[0]):
            jogo_sel_ninja.iniciar_jogo(tela, camera, hands)

        # Card 2: Maestro
        if desenhar_card("MAESTRO", "Controle a frequência", x_inicial + larg_card + espacamento, y_pos, larg_card, alt_card, CORES_CARDS[1]):
            jogo_osciloscopio.iniciar_jogo(tela, camera, hands)

        # Card 3: Filtros
        if desenhar_card("FILTROS DE IMAGEM", "Laboratório de PDI", x_inicial + 2*(larg_card + espacamento), y_pos, larg_card, alt_card, CORES_CARDS[2]):
            jogo_lab_pdi.iniciar_jogo(tela, camera, hands)

        # Rodapé
        rodape = fonte_sub.render("Desenvolvido por Vitor Augusto Tibério - SEL EESC/USP", True, (100, 100, 120))
        tela.blit(rodape, (LARGURA//2 - rodape.get_width()//2, 620))

        pygame.display.flip()

if __name__ == "__main__":
    main()