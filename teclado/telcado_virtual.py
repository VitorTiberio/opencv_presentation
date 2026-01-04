## Autor: Vitor Augusto Tibério - Estudante de Engenharia Elétrica - USP São Carlos ## 

## Importando as Bibliotecas ## 
import cv2
import mediapipe as mp
import pygame
import numpy as np
import sys

## Definindo as Funções ## 

def gerar_nota(frequencia, duracao=0.3, volume=0.5):
    """ Gera o array de áudio para uma nota específica """
    sample_rate = 44100
    n_samples = int(sample_rate * duracao)
    t = np.linspace(0, duracao, n_samples, False)
    # Onda senoidal básica
    onda = volume * np.sin(2 * np.pi * frequencia * t)
    # Aplica um pequeno fade-out para evitar estalos
    fade = np.linspace(1.0, 0.0, n_samples)
    audio = (onda * fade * 32767).astype(np.int16)
    return np.column_stack((audio, audio))

## Código Principal ## 

# Configurações de Áudio e Janela
LARGURA, ALTURA = 800, 600
pygame.init()
pygame.mixer.init(frequency=44100, size=-16, channels=2)
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Teclado Visual SEL - Recepção USP")

# Inicializa Visão com suporte para 2 mãos
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.8)
camera = cv2.VideoCapture(0)

# Definição das Notas (Dó, Ré, Mi, Fá, Sol, Lá, Si)
notas_freq = [261.63, 293.66, 329.63, 349.23, 392.00, 440.00, 493.88]
nomes_notas = ["DO", "RE", "MI", "FA", "SOL", "LA", "SI"]
sons = [pygame.sndarray.make_sound(gerar_nota(f)) for f in notas_freq]

# Configuração das Teclas
n_teclas = len(notas_freq)
largura_tecla = LARGURA // n_teclas

# Dicionário para rastrear o estado de cada mão (evitar repetição infinita)
# Chaves: 0 para a primeira mão, 1 para a segunda mão detectada
maos_estado = {-1: -1, 0: -1, 1: -1} 

clock = pygame.time.Clock()

while True:
    tela.fill((255, 255, 255))
    
    sucesso, frame = camera.read()
    if not sucesso: break
    
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    resultado = hands.process(rgb_frame)

    # Desenha o teclado 
    for i in range(n_teclas):
        # Verifica se alguma mão está pressionando esta tecla para mudar a cor
        pressionada = (i in maos_estado.values())
        cor = (200, 200, 200) if pressionada else (255, 255, 255)
        
        rect = pygame.Rect(i * largura_tecla, 100, largura_tecla - 5, 400)
        pygame.draw.rect(tela, cor, rect, border_radius=10)
        pygame.draw.rect(tela, (0, 0, 0), rect, 2, border_radius=10)
        
        fonte = pygame.font.SysFont("Consolas", 25, bold=True)
        txt = fonte.render(nomes_notas[i], True, (50, 50, 50))
        tela.blit(txt, (i * largura_tecla + largura_tecla//4, 450))

    # Lógica de detecção (mãos simultâneas)
    teclas_ativas_neste_frame = {0: -1, 1: -1}
    
    if resultado.multi_hand_landmarks:
        # Itera sobre as mãos detectadas (máximo 2)
        for idx, hand_landmarks in enumerate(resultado.multi_hand_landmarks):
            if idx > 1: break # Segurança para não ultrapassar o dicionário
            
            # Ponto 8 -- ponta do dedo indicador!!!
            dedo = hand_landmarks.landmark[8]
            px, py = int(dedo.x * LARGURA), int(dedo.y * ALTURA)
            
            # Desenha cursor diferente para cada mão
            cor_cursor = (0, 102, 204) if idx == 0 else (200, 0, 0)
            pygame.draw.circle(tela, cor_cursor, (px, py), 15)

            # Verifica se o dedo está na área das teclas
            if 100 < py < 500:
                indice_tecla = px // largura_tecla
                if 0 <= indice_tecla < n_teclas:
                    teclas_ativas_neste_frame[idx] = indice_tecla
                    
                    # Toca a nota se a mão idx acabou de entrar nesta tecla
                    if teclas_ativas_neste_frame[idx] != maos_estado[idx]:
                        sons[indice_tecla].play()
                        maos_estado[idx] = indice_tecla

    # Se a mão saiu de uma tecla ou da área, reseta o estado daquela mão
    for idx in [0, 1]:
        if teclas_ativas_neste_frame[idx] == -1:
            maos_estado[idx] = -1

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            camera.release()
            pygame.quit()
            sys.exit()

    pygame.display.flip()
    clock.tick(60)
