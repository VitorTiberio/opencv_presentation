## Autor: Vitor Augusto Tibério - Estudante de Engenharia Elétrica - USP São Carlos ## 

## Importando as Bibliotecas ## 
import cv2
import pygame
import sys
import numpy as np

## Definindo as Funções de Filtros ## 

def aplicar_filtro(frame, tipo):
    if tipo == "Original":
        return frame
    
    elif tipo == "Cinza":
        cinza = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return cv2.cvtColor(cinza, cv2.COLOR_GRAY2BGR)
    
    elif tipo == "Negativo":
        return cv2.bitwise_not(frame)
    
    elif tipo == "Canny (Bordas)":
        bordas = cv2.Canny(frame, 100, 200)
        return cv2.cvtColor(bordas, cv2.COLOR_GRAY2BGR)
    
    elif tipo == "Blur (Desfoque)":
        return cv2.GaussianBlur(frame, (15, 15), 0)
    
    elif tipo == "Sepia":
        kernel = np.array([[0.272, 0.534, 0.131],
                           [0.349, 0.686, 0.168],
                           [0.393, 0.769, 0.189]])
        return cv2.transform(frame, kernel)

    elif tipo == "Binarização":
        cinza = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        _, bina = cv2.threshold(cinza, 127, 255, cv2.THRESH_BINARY)
        return cv2.cvtColor(bina, cv2.COLOR_GRAY2BGR)

    elif tipo == "Laplaciano":
        # Operador de segunda ordem para realce de bordas
        lap = cv2.Laplacian(frame, cv2.CV_64F).astype(np.uint8)
        return lap

    elif tipo == "Cores Quentes":
        # Mapa de cores estilo inspeção térmica
        return cv2.applyColorMap(frame, cv2.COLORMAP_JET)

    elif tipo == "Cartoon":
        cinza = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cinza = cv2.medianBlur(cinza, 5)
        bordas = cv2.adaptiveThreshold(cinza, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
        cor = cv2.bilateralFilter(frame, 9, 300, 300)
        return cv2.bitwise_and(cor, cor, mask=bordas)

    return frame

def desenhar_botao(texto, x, y, largura, altura, ativo, tela, fonte):
    mouse = pygame.mouse.get_pos()
    clique = pygame.mouse.get_pressed()
    
    cor = (0, 102, 204) if ativo else (60, 60, 60)
    if x + largura > mouse[0] > x and y + altura > mouse[1] > y:
        cor = (0, 150, 255)
        if clique[0] == 1:
            pygame.time.delay(150)
            return True

    pygame.draw.rect(tela, cor, (x, y, largura, altura), border_radius=8)
    txt_surf = fonte.render(texto, True, (255, 255, 255))
    txt_rect = txt_surf.get_rect(center=(x + largura/2, y + altura/2))
    tela.blit(txt_surf, txt_rect)
    return False

## Código Principal ## 

LARGURA, ALTURA = 1050, 700
pygame.init()
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Laboratório de Filtros SEL - USP São Carlos")
fonte = pygame.font.SysFont("Consolas", 16, bold=True)
fonte_titulo = pygame.font.SysFont("Consolas", 24, bold=True)

camera = cv2.VideoCapture(0)
filtros_lista = [
    "Original", "Cinza", "Negativo", "Canny (Bordas)", 
    "Blur (Desfoque)", "Sepia", "Binarização", 
    "Laplaciano", "Cores Quentes", "Cartoon"
]
filtro_atual = "Original"

clock = pygame.time.Clock()

while True:
    tela.fill((20, 20, 25)) 
    
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            camera.release()
            pygame.quit()
            sys.exit()

    # Processamento de Vídeo
    sucesso, frame = camera.read()
    if sucesso:
        frame = cv2.flip(frame, 1)
        frame_filtrado = aplicar_filtro(frame, filtro_atual)
        
        # Converte BGR (OpenCV) para RGB (Pygame)
        frame_rgb = cv2.cvtColor(frame_filtrado, cv2.COLOR_BGR2RGB)
        frame_pygame = pygame.surfarray.make_surface(np.transpose(frame_rgb, (1, 0, 2)))
        # Redimensiona mantendo a proporção
        frame_visual = pygame.transform.scale(frame_pygame, (720, 540))
        tela.blit(frame_visual, (30, 80))

    # Definição da Interface Lateral (Botões)
    pygame.draw.rect(tela, (40, 40, 45), (780, 0, 270, ALTURA)) # Painel lateral
    for i, nome_filtro in enumerate(filtros_lista):
        if desenhar_botao(nome_filtro, 800, 50 + (i * 62), 230, 45, filtro_atual == nome_filtro, tela, fonte):
            filtro_atual = nome_filtro

    # Escrevendo os Textos Informativos no Vídeo
    titulo = fonte_titulo.render("PROCESSAMENTO DIGITAL DE IMAGENS - SEL", True, (0, 150, 255))
    info = fonte.render(f"Filtro Aplicado: {filtro_atual}", True, (200, 200, 200))
    tela.blit(titulo, (30, 20))
    tela.blit(info, (30, 55))

    pygame.display.flip()
    clock.tick(30)
