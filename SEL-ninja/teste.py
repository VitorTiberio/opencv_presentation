## Autor: Vitor Augusto Tibério - Estudante de Engenharia Elétrica

## Importando as Bibliotecas ## 

import cv2 as cv
import mediapipe as mp 
import pygame 
import random 

## Configuração das condições de vídeo ## 

LARGURA, ALTURA = 800, 600
FPS = 60

## Configuração do Mediapipe ## 
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7) ## grau de confiaça da detectabilidade

## Configuração do PyGame ##

pygame.init()
tela = pygame.display.set_mode((LARGURA, ALTURA))
clock = pygame.time.Clock()
camera = cv.VideoCapture(0)

class Fruta:
    def __init__(self):
        self.x = random.randint(100, LARGURA - 100)
        self.y = ALTURA
        self.vel_y = random.randint(-18, -12) # Força do pulo
        self.vel_x = random.randint(-3, 3)
        self.cortada = False

    def atualizar(self):
        self.x += self.vel_x
        self.y += self.vel_y
        self.vel_y += 0.5 # Gravidade

    def desenhar(self):
        cor = (0, 255, 0) if not self.cortada else (255, 0, 0)
        pygame.draw.circle(tela, cor, (int(self.x), int(self.y)), 30)

frutas = [Fruta()]
pontos = 0
rodando = True

while rodando:
    tela.fill((255, 255, 255)) # Fundo branco
    
    # Captura do OpenCV
    sucesso, frame = camera.read()
    if not sucesso: break
    frame = cv.flip(frame, 1) # Espelha a imagem
    rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    resultado = hands.process(rgb_frame)

    pos_dedo = None
    if resultado.multi_hand_landmarks:
        for hand_landmarks in resultado.multi_hand_landmarks:
            # Pegamos o ponto 8 (ponta do dedo indicador)
            dedo = hand_landmarks.landmark[8]
            pos_dedo = (int(dedo.x * LARGURA), int(dedo.y * ALTURA))
            pygame.draw.circle(tela, (0, 0, 255), pos_dedo, 10) # Desenha o cursor

    # Lógica das Frutas
    for fruta in frutas[:]:
        fruta.atualizar()
        fruta.desenhar()

        # Checa colisão com o dedo
        if pos_dedo and not fruta.cortada:
            distancia = ((fruta.x - pos_dedo[0])**2 + (fruta.y - pos_dedo[1])**2)**0.5
            if distancia < 40:
                fruta.cortada = True
                pontos += 1

        # Remove frutas que saíram da tela
        if fruta.y > ALTURA + 50:
            frutas.remove(fruta)

    # Cria novas frutas aleatoriamente
    if random.random() < 0.03:
        frutas.append(Fruta())

    # Eventos e Atualização
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    pygame.display.flip()
    clock.tick(FPS)

camera.release()
pygame.quit()
