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
LARGURA, ALTURA = 1150, 750
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("JOGOS DE OPENCV - SEL - EESC/USP")

# Recursos Compartilhados (Inicialização Única)
camera = cv2.VideoCapture(0)
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7)

# Paleta de Cores Neon
COR_FUNDO = (15, 15, 25)
BRANCO = (255, 255, 255)
AMARELO_ARCADE = (255, 200, 0)
CINZA_TEXTO = (160, 160, 170)

# Configuração dos Cards (Nome, Sublegenda, Cor Neon)
CARDS_INFO = [
    ("SEL NINJA", "Capture os componentes!", (255, 40, 80)),      # Vermelho Neon
    ("MAESTRO", "Controle a frequência e amplitude no laboratório de sinais", (0, 180, 255)), # Azul Neon
    ("FILTROS DE IMAGENS", "Laboratório PDI em tempo real", (40, 255, 150)) # Verde Neon
]

# Fontes
fonte_arcade = pygame.font.SysFont("Impact", 90)
fonte_card_titulo = pygame.font.SysFont("Impact", 32)
fonte_card_sub = pygame.font.SysFont("Verdana", 14, italic=True)
fonte_footer = pygame.font.SysFont("Consolas", 16)

def desenhar_card_premium(index, info, x, y, largura, altura):
    titulo, sub, cor_neon = info
    mouse = pygame.mouse.get_pos()
    clique = pygame.mouse.get_pressed()
    
    rect = pygame.Rect(x, y, largura, altura)
    is_hover = rect.collidepoint(mouse)
    
    # Sombra/Brilho externo se estiver com o mouse em cima
    if is_hover:
        for i in range(1, 15): # Efeito de Glow gradativo
            alpha = 150 // i
            s = pygame.Surface((largura + i*2, altura + i*2), pygame.SRCALPHA)
            pygame.draw.rect(s, (*cor_neon, alpha), (0, 0, largura + i*2, altura + i*2), border_radius=20)
            tela.blit(s, (x - i, y - i))

    # Fundo do Card (Gradiente escuro)
    cor_fundo_card = (35, 35, 50) if is_hover else (25, 25, 40)
    pygame.draw.rect(tela, cor_fundo_card, rect, border_radius=15)
    
    # Borda Neon
    largura_borda = 4 if is_hover else 2
    pygame.draw.rect(tela, cor_neon, rect, border_radius=15, width=largura_borda)

    # Textos Renderizados
    # Título (Impact)
    txt_t = fonte_card_titulo.render(titulo, True, BRANCO)
    tela.blit(txt_t, (x + (largura - txt_t.get_width())//2, y + 60))
    
    # Sublegenda (Quebra de linha manual se for muito grande)
    palavras = sub.split(' ')
    linha1 = " ".join(palavras[:len(palavras)//2])
    linha2 = " ".join(palavras[len(palavras)//2:])
    
    sub1 = fonte_card_sub.render(linha1, True, CINZA_TEXTO)
    sub2 = fonte_card_sub.render(linha2, True, CINZA_TEXTO)
    
    tela.blit(sub1, (x + (largura - sub1.get_width())//2, y + 120))
    tela.blit(sub2, (x + (largura - sub2.get_width())//2, y + 140))

    if is_hover and clique[0] == 1:
        pygame.time.delay(250)
        return True
    return False

def main():
    while True:
        tela.fill(COR_FUNDO)
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                camera.release()
                pygame.quit()
                sys.exit()

        # Título
        txt_titulo = fonte_arcade.render("JOGOS DE OPENCV", True, AMARELO_ARCADE)
        tela.blit(txt_titulo, (LARGURA//2 - txt_titulo.get_width()//2, 70))
        
        txt_sub = fonte_footer.render("Selecione qual jogo quer jogar:", True, BRANCO)
        tela.blit(txt_sub, (LARGURA//2 - txt_sub.get_width()//2, 170))

        # Posicionamento dos Cards
        larg_c, alt_c = 320, 240
        espacamento = 40
        x_start = (LARGURA - (3 * larg_c + 2 * espacamento)) // 2
        
        # Execução dos Módulos
        if desenhar_card_premium(0, CARDS_INFO[0], x_start, 280, larg_c, alt_c):
            jogo_sel_ninja.iniciar_jogo(tela, camera, hands)
            
        if desenhar_card_premium(1, CARDS_INFO[1], x_start + larg_c + espacamento, 280, larg_c, alt_c):
            jogo_osciloscopio.iniciar_jogo(tela, camera, hands)
            
        if desenhar_card_premium(2, CARDS_INFO[2], x_start + 2*(larg_c + espacamento), 280, larg_c, alt_c):
            jogo_lab_pdi.iniciar_jogo(tela, camera, hands)

        # Autoria
        footer = fonte_footer.render("Autor: Vitor Augusto Tibério - SEL - USP SÃO CARLOS | 2026", True, (80, 80, 100))
        tela.blit(footer, (LARGURA//2 - footer.get_width()//2, 650))

        pygame.display.flip()

if __name__ == "__main__":
    main()
