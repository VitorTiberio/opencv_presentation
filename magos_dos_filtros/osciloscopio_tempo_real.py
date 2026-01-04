## Autor: Vitor Augusto Tibério - Estudante de Engenharia Elétrica - USP São Carlos ## 

## Importando as Bibliotecas ## 
import cv2
import mediapipe as mp
import pygame
import numpy as np
import sys

## Definindo as Funções ## 

def gerar_onda_senoidal(frequencia, volume, sample_rate=44100):
    """ Gera um array de áudio para uma onda senoidal pura """
    duracao = 0.1 
    n_samples = int(sample_rate * duracao)
    t = np.linspace(0, duracao, n_samples, False)
    onda = volume * np.sin(2 * np.pi * frequencia * t)
    audio = (onda * 32767).astype(np.int16)
    return np.column_stack((audio, audio))

## Código Principal ## 

# Configurações de Tela e Áudio
LARGURA, ALTURA = 800, 600
pygame.init()
pygame.mixer.init(frequency=44100, size=-16, channels=2)
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Osciloscópio em tempo real - SEL USP")
fonte = pygame.font.SysFont("Consolas", 22)

# Inicializa Visão
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7)
camera = cv2.VideoCapture(0)

clock = pygame.time.Clock()
frequencia_atual = 440
volume_atual = 0.5

while True:
    tela.fill((255, 255, 255)) # Fundo Branco
    
    sucesso, frame = camera.read()
    if not sucesso: break
    
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    resultado = hands.process(rgb_frame)
    
    maos_detectadas = {}
    if resultado.multi_hand_landmarks:
        for idx, hand_landmarks in enumerate(resultado.multi_handedness):
            label = hand_landmarks.classification[0].label
            coords = resultado.multi_hand_landmarks[idx].landmark[8]
            maos_detectadas[label] = (int(coords.x * LARGURA), int(coords.y * ALTURA))

    # Lógica de Controle (dependendo da mão que foi detectada)
    if "Right" in maos_detectadas:
        frequencia_atual = 100 + (maos_detectadas["Right"][0] / LARGURA) * 900
        pygame.draw.circle(tela, (0, 102, 204), maos_detectadas["Right"], 20)
        
    if "Left" in maos_detectadas:
        volume_atual = max(0, min(1, 1 - (maos_detectadas["Left"][1] / ALTURA)))
        pygame.draw.circle(tela, (200, 0, 0), maos_detectadas["Left"], 20)

    # Plotagem da Senoide
    # Desenhando a senoide no meio da tela
    pontos_onda = []
    centro_y = ALTURA // 2
    
    for x in range(0, LARGURA, 2):
        # Escalonei a frequência para a visualização ficar bonita (independente do áudio)
        # Usei uma "frequência visual" baseada na frequência real
        escala_v = (frequencia_atual / 1000) * 0.5
        y = centro_y + int(volume_atual * 150 * np.sin(x * escala_v))
        pontos_onda.append((x, y))
    
    if len(pontos_onda) > 1:
        pygame.draw.lines(tela, (30, 30, 30), False, pontos_onda, 3)

    # Toca o som
    if len(maos_detectadas) > 0:
        som_array = gerar_onda_senoidal(frequencia_atual, volume_atual)
        som_pygame = pygame.sndarray.make_sound(som_array)
        som_pygame.play()

    # Interface
    txt_f = fonte.render(f"Frequência: {int(frequencia_atual)} Hz", True, (0, 102, 204))
    txt_v = fonte.render(f"Amplitude: {int(volume_atual * 100)}%", True, (200, 0, 0))
    tela.blit(txt_f, (20, 20))
    tela.blit(txt_v, (20, 50))

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            camera.release()
            pygame.quit()
            sys.exit()

    pygame.display.flip()
    clock.tick(30)
