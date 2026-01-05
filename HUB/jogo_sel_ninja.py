## Autor: Vitor Augusto Tibério - Estudante de Engenharia Elétrica - USP São Carlos 

import cv2
import mediapipe as mp
import pygame
import random
import sys

def carregar_imagem(nome, tamanho=(80, 80)):
    try:
        img = pygame.image.load(nome).convert_alpha()
        return pygame.transform.scale(img, tamanho)
    except:
        surf = pygame.Surface(tamanho)
        surf.fill((200, 0, 0) if "sasel" in nome else (0, 200, 0))
        return surf

class Item:
    def __init__(self, imgs_bons, img_vilao, LARGURA, ALTURA):
        self.e_vilao = random.random() < 0.2
        self.imagem = img_vilao if self.e_vilao else random.choice(imgs_bons)
        self.rect = self.imagem.get_rect(midtop=(random.randint(100, LARGURA-100), ALTURA))
        self.vel_y = random.randint(-22, -16)
        self.vel_x = random.randint(-4, 4)
        self.ativo = True

    def atualizar(self):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        self.vel_y += 0.6

    def desenhar(self, superficie):
        if self.ativo: superficie.blit(self.imagem, self.rect)

def iniciar_jogo(tela, camera, hands):
    LARGURA, ALTURA = tela.get_size()
    clock = pygame.time.Clock()
    fonte = pygame.font.SysFont("Consolas", 30)
    
    # Ativos
    pasta = "imagens/"
    imgs_bons = [carregar_imagem(f"{pasta}{f}") for f in ['resistor.png', 'capacitor.png', 'led.png', 'transistor.png']]
    img_vilao = carregar_imagem(f"{pasta}sasel.png", (90, 90))
    img_cursor = carregar_imagem(f"{pasta}chave_fenda.png", (100, 100))

    itens, pontos, vidas, tempo_restante = [], 0, 3, 60
    frame_count, tempo_pisca = 0, 0

    rodando = True
    while rodando:
        if tempo_pisca > 0:
            tela.fill((255, 0, 0))
            tempo_pisca -= 1
        else:
            tela.fill((255, 255, 255))

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT: return "SAIR"
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE: rodando = False

        sucesso, frame = camera.read()
        if sucesso:
            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            resultado = hands.process(rgb_frame)
            
            pos_dedo = None
            if resultado.multi_hand_landmarks:
                dedo = resultado.multi_hand_landmarks[0].landmark[8]
                pos_dedo = (int(dedo.x * LARGURA), int(dedo.y * ALTURA))

            frame_count += 1
            if frame_count >= 60:
                tempo_restante -= 1
                frame_count = 0

            if random.random() < 0.05: itens.append(Item(imgs_bons, img_vilao, LARGURA, ALTURA))

            for item in itens[:]:
                item.atualizar()
                item.desenhar(tela)
                if pos_dedo and item.rect.collidepoint(pos_dedo) and item.ativo:
                    item.ativo = False
                    if item.e_vilao: vidas -= 1; tempo_pisca = 5
                    else: pontos += 10
                if item.rect.y > ALTURA + 50: itens.remove(item)

            if pos_dedo: tela.blit(img_cursor, (pos_dedo[0] - 50, pos_dedo[1] - 50))

        # HUD
        tela.blit(fonte.render(f"PONTOS: {pontos}", True, (50, 50, 50)), (20, 20))
        tela.blit(fonte.render(f"VIDAS: {vidas}", True, (200, 0, 0)), (20, 55))
        tela.blit(fonte.render(f"TEMPO: {tempo_restante}s", True, (0, 102, 204)), (LARGURA - 180, 20))

        if vidas <= 0 or tempo_restante <= 0: rodando = False

        pygame.display.flip()
        clock.tick(60)