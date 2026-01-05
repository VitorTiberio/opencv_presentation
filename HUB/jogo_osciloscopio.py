import cv2
import pygame
import numpy as np

def gerar_onda_senoidal(frequencia, volume):
    duracao, sample_rate = 0.1, 44100
    n_samples = int(sample_rate * duracao)
    t = np.linspace(0, duracao, n_samples, False)
    onda = volume * np.sin(2 * np.pi * frequencia * t)
    audio = (onda * 32767).astype(np.int16)
    return np.column_stack((audio, audio))

def iniciar_jogo(tela, camera, hands):
    LARGURA, ALTURA = tela.get_size()
    clock = pygame.time.Clock()
    fonte = pygame.font.SysFont("Consolas", 22)
    frequencia_atual, volume_atual = 440, 0.5

    rodando = True
    while rodando:
        tela.fill((255, 255, 255))
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT: return "SAIR"
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE: rodando = False

        sucesso, frame = camera.read()
        if sucesso:
            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            resultado = hands.process(rgb_frame)
            
            maos = {}
            if resultado.multi_hand_landmarks:
                for idx, hand_landmarks in enumerate(resultado.multi_handedness):
                    label = hand_landmarks.classification[0].label
                    coords = resultado.multi_hand_landmarks[idx].landmark[8]
                    maos[label] = (int(coords.x * LARGURA), int(coords.y * ALTURA))

            if "Right" in maos:
                frequencia_atual = 100 + (maos["Right"][0] / LARGURA) * 900
                pygame.draw.circle(tela, (0, 102, 204), maos["Right"], 20)
            if "Left" in maos:
                volume_atual = max(0, min(1, 1 - (maos["Left"][1] / ALTURA)))
                pygame.draw.circle(tela, (200, 0, 0), maos["Left"], 20)

            # Desenho da Onda
            pontos_onda = []
            for x in range(0, LARGURA, 2):
                escala_v = (frequencia_atual / 1000) * 0.5
                y = (ALTURA//2) + int(volume_atual * 150 * np.sin(x * escala_v))
                pontos_onda.append((x, y))
            if len(pontos_onda) > 1: pygame.draw.lines(tela, (30, 30, 30), False, pontos_onda, 3)

            if maos:
                som = pygame.sndarray.make_sound(gerar_onda_senoidal(frequencia_atual, volume_atual))
                som.play()

        tela.blit(fonte.render(f"Frequência: {int(frequencia_atual)} Hz", True, (0, 102, 204)), (20, 20))
        tela.blit(fonte.render(f"Amplitude: {int(volume_atual * 100)}%", True, (200, 0, 0)), (20, 50))
        
        pygame.display.flip()
        clock.tick(30)