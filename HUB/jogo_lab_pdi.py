import cv2
import pygame
import numpy as np

def aplicar_filtro(frame, tipo):
    if tipo == "Cinza": return cv2.cvtColor(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), cv2.COLOR_GRAY2BGR)
    if tipo == "Negativo": return cv2.bitwise_not(frame)
    if tipo == "Canny (Bordas)": return cv2.cvtColor(cv2.Canny(frame, 100, 200), cv2.COLOR_GRAY2BGR)
    if tipo == "Blur (Desfoque)": return cv2.GaussianBlur(frame, (15, 15), 0)
    if tipo == "Binarização": 
        _, bina = cv2.threshold(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), 127, 255, cv2.THRESH_BINARY)
        return cv2.cvtColor(bina, cv2.COLOR_GRAY2BGR)
    return frame

def iniciar_jogo(tela, camera, hands):
    LARGURA, ALTURA = tela.get_size()
    filtros = ["Original", "Cinza", "Negativo", "Canny (Bordas)", "Blur (Desfoque)", "Binarização"]
    filtro_atual = "Original"
    fonte = pygame.font.SysFont("Consolas", 18, bold=True)

    rodando = True
    while rodando:
        tela.fill((20, 20, 25))
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT: return "SAIR"
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE: rodando = False
                # Troca filtro nas setas
                if evento.key == pygame.K_RIGHT:
                    idx = (filtros.index(filtro_atual) + 1) % len(filtros)
                    filtro_atual = filtros[idx]

        sucesso, frame = camera.read()
        if sucesso:
            frame = aplicar_filtro(cv2.flip(frame, 1), filtro_atual)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            surf = pygame.surfarray.make_surface(np.transpose(frame_rgb, (1, 0, 2)))
            tela.blit(pygame.transform.scale(surf, (800, 600)), (100, 50))

        tela.blit(fonte.render(f"FILTRO: {filtro_atual} (Use as setas - ESC p/ sair)", True, (255, 255, 255)), (20, 20))
        pygame.display.flip()