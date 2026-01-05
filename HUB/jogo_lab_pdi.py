## Autor: Vitor Augusto Tibério - Estudante de Engenharia Elétrica - USP São Carlos ## 

import cv2
import pygame
import numpy as np
import sys

def aplicar_filtro(frame, tipo):
    """ Centraliza todas as transformações de matrizes de imagem """
    if tipo == "Original": return frame
    if tipo == "Cinza":
        return cv2.cvtColor(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), cv2.COLOR_GRAY2BGR)
    if tipo == "Negativo":
        return cv2.bitwise_not(frame)
    if tipo == "Canny (Bordas)":
        return cv2.cvtColor(cv2.Canny(frame, 100, 200), cv2.COLOR_GRAY2BGR)
    if tipo == "Blur (Desfoque)":
        return cv2.GaussianBlur(frame, (15, 15), 0)
    if tipo == "Sepia":
        k = np.array([[0.272, 0.534, 0.131], [0.349, 0.686, 0.168], [0.393, 0.769, 0.189]])
        return cv2.transform(frame, k)
    if tipo == "Binarização":
        _, b = cv2.threshold(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), 127, 255, cv2.THRESH_BINARY)
        return cv2.cvtColor(b, cv2.COLOR_GRAY2BGR)
    if tipo == "Laplaciano":
        return cv2.Laplacian(frame, cv2.CV_64F).astype(np.uint8)
    if tipo == "Cores Quentes":
        return cv2.applyColorMap(frame, cv2.COLORMAP_JET)
    if tipo == "Cartoon":
        c = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        c = cv2.medianBlur(c, 5)
        b = cv2.adaptiveThreshold(c, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
        cor = cv2.bilateralFilter(frame, 9, 300, 300)
        return cv2.bitwise_and(cor, cor, mask=b)
    return frame

def desenhar_botao_filtro(texto, x, y, largura, altura, ativo, tela, fonte):
    """ Desenha os botões interativos na lateral """
    mouse = pygame.mouse.get_pos()
    clique = pygame.mouse.get_pressed()
    
    cor = (0, 180, 255) if ativo else (60, 60, 75)
    if x + largura > mouse[0] > x and y + altura > mouse[1] > y:
        cor = (100, 200, 255)
        if clique[0] == 1:
            pygame.time.delay(150)
            return True

    pygame.draw.rect(tela, cor, (x, y, largura, altura), border_radius=8)
    txt = fonte.render(texto, True, (255, 255, 255))
    tela.blit(txt, (x + (largura - txt.get_width())//2, y + (altura - txt.get_height())//2))
    return False

def iniciar_jogo(tela, camera, hands):
    LARGURA, ALTURA = tela.get_size()
    clock = pygame.time.Clock()
    fonte = pygame.font.SysFont("Consolas", 16, bold=True)
    
    filtros_lista = [
        "Original", "Cinza", "Negativo", "Canny (Bordas)", 
        "Blur (Desfoque)", "Sepia", "Binarização", 
        "Laplaciano", "Cores Quentes", "Cartoon"
    ]
    filtro_atual = "Original"

    rodando = True
    while rodando:
        tela.fill((20, 20, 30))
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT: return "SAIR"
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                rodando = False

        # Captura e Processamento
        sucesso, frame = camera.read()
        if sucesso:
            frame = cv2.flip(frame, 1)
            frame_filtrado = aplicar_filtro(frame, filtro_atual)
            
            # Converte e redimensiona para o espaço da tela (deixando margem para botões)
            frame_rgb = cv2.cvtColor(frame_filtrado, cv2.COLOR_BGR2RGB)
            surf = pygame.surfarray.make_surface(np.transpose(frame_rgb, (1, 0, 2)))
            video_visual = pygame.transform.scale(surf, (750, 560))
            tela.blit(video_visual, (30, 80))

        # Painel Lateral de Botões
        pygame.draw.rect(tela, (40, 40, 55), (810, 0, 290, ALTURA)) # Fundo do painel
        for i, nome in enumerate(filtros_lista):
            if desenhar_botao_filtro(nome, 830, 60 + (i * 62), 240, 45, filtro_atual == nome, tela, fonte):
                filtro_atual = nome

        # Textos de Cabeçalho
        titulo = fonte.render(f"MODO ATIVO: {filtro_atual}", True, (0, 180, 255))
        tela.blit(titulo, (30, 30))
        tela.blit(fonte.render("ESC para Voltar ao Menu", True, (150, 150, 150)), (30, 55))

        pygame.display.flip()
        clock.tick(30)
