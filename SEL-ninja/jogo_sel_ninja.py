## Autor: Vitor Augusto Tibério - Estudante de Engenharia Elétrica - USP São Carlos ## 

## Importando as Bibliotecas ## 

import cv2
import mediapipe as mp
import pygame
import random
import sys
import os 

## Definindo as Funções ## 

def carregar_imagem(nome, tamanho=(80, 80)):
    try:
        img = pygame.image.load(nome).convert_alpha()
        return pygame.transform.scale(img, tamanho)
    except:
        # Fallback: cria um bloco colorido se a imagem faltar
        surf = pygame.Surface(tamanho)
        surf.fill((200, 0, 0) if "curto" in nome else (0, 200, 0))
        return surf

def tratar_camera(camera, hands, LARGURA, ALTURA):
    sucesso, frame = camera.read()
    if not sucesso:
        return None, None
    
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    resultado = hands.process(rgb_frame)
    
    pos_dedo = None
    if resultado.multi_hand_landmarks:
        # Ponto 8 é a ponta do indicador
        dedo = resultado.multi_hand_landmarks[0].landmark[8]
        pos_dedo = (int(dedo.x * LARGURA), int(dedo.y * ALTURA))
        
    return pos_dedo, frame

## Definindo as Classes ## 

class Item:
    def __init__(self, imgs_bons, img_vilao, largura_tela, altura_tela):
        self.e_vilao = random.random() < 0.2  # 20% de chance de ser curto-circuito
        self.imagem = img_vilao if self.e_vilao else random.choice(imgs_bons)
        self.largura_tela = largura_tela
        self.altura_tela = altura_tela
        
        # Posição inicial e física
        self.rect = self.imagem.get_rect(midtop=(random.randint(100, largura_tela-100), altura_tela))
        self.vel_y = random.randint(-22, -16)
        self.vel_x = random.randint(-4, 4)
        self.ativo = True

    def atualizar(self):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        self.vel_y += 0.6  # Gravidade

    def desenhar(self, superficie):
        if self.ativo:
            superficie.blit(self.imagem, self.rect)

## Código Principal ## 

# Configurações da Tela # 
LARGURA, ALTURA = 800, 600
pygame.init()
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Secretaria Acadêmica da Engenharia Elétrica - SEL Ninja")
clock = pygame.time.Clock()

# Inicializa Mediapipe e Visão
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
camera = cv2.VideoCapture(0)

# Carrega Ativos
pasta = "imagens/"
imgs_bons = [carregar_imagem(f"{pasta}{f}") for f in ['resistor.png', 'capacitor.png', 'led.png', 'transistor.png']]
img_vilao = carregar_imagem(f"{pasta}curto_circuito.png", (90, 90))
img_cursor = carregar_imagem(f"{pasta}ponta_de_prova.png", (100, 100))

# Variáveis de Estado
itens = []
pontos = 0
vidas = 3
fonte = pygame.font.SysFont("Consolas", 30)

# Loop do Jogo
while vidas > 0:
    tela.fill((30, 30, 30))
    
    # Processa Entrada (Câmera e Teclado)
    pos_dedo, _ = tratar_camera(camera, hands, LARGURA, ALTURA)
    
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Atualiza e Desenha Itens
    for item in itens[:]:
        item.atualizar()
        item.desenhar(tela)

        # Verifica Colisão
        if pos_dedo and item.rect.collidepoint(pos_dedo) and item.ativo:
            item.ativo = False
            if item.e_vilao:
                vidas -= 1
            else:
                pontos += 10

        # Limpeza de memória
        if item.rect.y > ALTURA + 50:
            itens.remove(item)

    # Spawner de Itens
    if random.random() < 0.05:
        itens.append(Item(imgs_bons, img_vilao, LARGURA, ALTURA))

    # Desenha Cursor (Ponta de Prova)
    if pos_dedo:
        tela.blit(img_cursor, (pos_dedo[0] - 50, pos_dedo[1] - 50))

    # HUD
    txt = fonte.render(f"PONTOS: {pontos} | VIDAS: {vidas}", True, (255, 255, 255))
    tela.blit(txt, (20, 20))

    pygame.display.flip()
    clock.tick(60)

# Finalização
camera.release()
pygame.quit()
