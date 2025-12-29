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
        # cria um bloco colorido se a imagem não carregar
        surf = pygame.Surface(tamanho)
        surf.fill((200, 0, 0) if "sasel" in nome else (0, 200, 0))
        return surf

def tratar_camera(camera, hands, LARGURA, ALTURA):
    sucesso, frame = camera.read()
    if not sucesso:
        return None, None
    
    frame = cv2.flip(frame, 1) #flipa a câmera
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    resultado = hands.process(rgb_frame)
    
    pos_dedo = None
    if resultado.multi_hand_landmarks:
        # Ponto 8 é a ponta do indicador!!!!!!!
        dedo = resultado.multi_hand_landmarks[0].landmark[8]
        pos_dedo = (int(dedo.x * LARGURA), int(dedo.y * ALTURA))
        
    return pos_dedo, frame

def desenhar_botao(texto, x, y, largura, altura, cor_normal, cor_hover, tela, fonte):
    mouse = pygame.mouse.get_pos()
    clique = pygame.mouse.get_pressed()
    
    if x + largura > mouse[0] > x and y + altura > mouse[1] > y:
        pygame.draw.rect(tela, cor_hover, (x, y, largura, altura), border_radius=12)
        if clique[0] == 1:
            pygame.time.delay(150)
            return True
    else:
        pygame.draw.rect(tela, cor_normal, (x, y, largura, altura), border_radius=12)
    
    txt_surf = fonte.render(texto, True, (255, 255, 255))
    txt_rect = txt_surf.get_rect(center=(x + largura/2, y + altura/2))
    tela.blit(txt_surf, txt_rect)
    return False

## Definindo as Classes ## 

class Item:
    def __init__(self, imgs_bons, img_vilao, largura_tela, altura_tela):
        self.e_vilao = random.random() < 0.2  # 20% de chance de ser o vilão (SASEL)
        self.imagem = img_vilao if self.e_vilao else random.choice(imgs_bons)
        self.largura_tela = largura_tela
        self.altura_tela = altura_tela
        
        # Posição inicial (surge de baixo para cima)
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

# Inicializa Mediapipe e Visão #
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
camera = cv2.VideoCapture(0)

# Carrega as imagens que aparecerão no jogo #
pasta = "imagens/"
imgs_bons = [carregar_imagem(f"{pasta}{f}") for f in ['resistor.png', 'capacitor.png', 'led.png', 'transistor.png']]
img_vilao = carregar_imagem(f"{pasta}sasel.png", (90, 90))
img_cursor = carregar_imagem(f"{pasta}chave_fenda.png", (100, 100))

# Variáveis de Estado #
itens = []
pontos = 0
vidas = 3
tempo_total = 60 # Tempo de jogo em segundos
tempo_restante = tempo_total
frame_count = 0
tempo_pisca = 0
estado = "MENU"

fonte = pygame.font.SysFont("Consolas", 30)
fonte_titulo = pygame.font.SysFont("Consolas", 60, bold=True)
fonte_perdeu = pygame.font.SysFont("Consolas", 80, bold=True)

# Loop do Jogo #

while True:
    # Lógica de Cor de Fundo (Piscar Vermelho)
    if tempo_pisca > 0:
        tela.fill((255, 0, 0))
        tempo_pisca -= 1
    else:
        tela.fill((255, 255, 255))
    
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            camera.release()
            pygame.quit()
            sys.exit()

    if estado == "MENU":
        txt_titulo = fonte_titulo.render("SEL NINJA", True, (0, 102, 204))
        tela.blit(txt_titulo, (LARGURA//2 - 150, 150))
        
        if desenhar_botao("JOGAR", LARGURA//2 - 100, 350, 200, 60, (0, 150, 0), (0, 200, 0), tela, fonte):
            estado = "JOGANDO"
            pontos = 0
            vidas = 3
            tempo_restante = tempo_total
            frame_count = 0
            itens = []

    elif estado == "JOGANDO":
        # Processa a imagem da câmera
        pos_dedo, _ = tratar_camera(camera, hands, LARGURA, ALTURA)
        
        # Controle de tempo
        frame_count += 1
        if frame_count >= 60: # Passou 1 segundo (a 60 FPS)
            tempo_restante -= 1
            frame_count = 0
        
        # Spawner de Itens
        if random.random() < 0.05:
            itens.append(Item(imgs_bons, img_vilao, LARGURA, ALTURA))

        # Atualiza e Desenha Itens
        for item in itens[:]:
            item.atualizar()
            item.desenhar(tela)

            if pos_dedo and item.rect.collidepoint(pos_dedo) and item.ativo:
                item.ativo = False
                if item.e_vilao:
                    vidas -= 1
                    tempo_pisca = 5
                else:
                    pontos += 10

            if item.rect.y > ALTURA + 50:
                itens.remove(item)

        if pos_dedo:
            tela.blit(img_cursor, (pos_dedo[0] - 50, pos_dedo[1] - 50))

        # HUD (Placar, Vidas e Tempo)
        txt_p = fonte.render(f"PONTOS: {pontos}", True, (50, 50, 50))
        txt_v = fonte.render(f"VIDAS: {vidas}", True, (200, 0, 0))
        txt_t = fonte.render(f"TEMPO: {tempo_restante}s", True, (0, 102, 204))
        
        tela.blit(txt_p, (20, 20))
        tela.blit(txt_v, (20, 55))
        tela.blit(txt_t, (LARGURA - 180, 20))

        # Checa Derrota ou Fim de Tempo
        if vidas <= 0 or tempo_restante <= 0:
            estado = "PERDEU"

    elif estado == "PERDEU":
        msg = "FIM DE TEMPO!" if tempo_restante <= 0 else "VOCÊ PERDEU!"
        txt_perdeu = fonte_perdeu.render(msg, True, (200, 0, 0))
        tela.blit(txt_perdeu, (LARGURA//2 - 250, 150))
        
        txt_final = fonte.render(f"PONTUAÇÃO FINAL: {pontos}", True, (50, 50, 50))
        tela.blit(txt_final, (LARGURA//2 - 150, 250))
        
        if desenhar_botao("TENTAR NOVAMENTE", LARGURA//2 - 150, 400, 300, 60, (0, 102, 204), (0, 150, 255), tela, fonte):
            estado = "JOGANDO"
            pontos = 0
            vidas = 3
            tempo_restante = tempo_total
            frame_count = 0
            itens = []

    pygame.display.flip()
    clock.tick(60)
