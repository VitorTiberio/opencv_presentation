## Autor: Vitor Augusto Tibério - Estudante de Engenharia Elétrica - USP São Carlos ## 

## Importando as Bilbiotecas ##  
import cv2
import mediapipe as mp
import serial
import time

## Configuração da Porta Serial -- pode dar ruim dependendo da porta USB que tá sendo usada. Alterar na serial.Serial a porta correta!!!!
try:
    esp32 = serial.Serial('COM3', 115200, timeout=1)
    time.sleep(2) # Espera a conexão estabilizar
    print("Conectado à ESP32!")
except:
    print("AVISO: ESP32 não conectada ou porta errada. O código vai rodar só visualmente.")
    esp32 = None

# Configurações do vídeo 
cap = cv2.VideoCapture(0)
mp_maos = mp.solutions.hands
maos = mp_maos.Hands(max_num_hands=1) # Detectar apenas 1 mão para não confundir
mp_desenho = mp.solutions.drawing_utils

# IDs dos pontos das pontas dos dedos no MediaPipe
ponta_dedos = [8, 12, 16, 20] # Indicador, Médio, Anelar, Mindinho

def contar_dedos(hand_landmarks):
    contador = 0
    # Se a ponta do dedão (4) estiver mais à direita/esquerda que a articulação (3)
    if hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x:
        contador += 1
    # Se a ponta do dedo (y) estiver "acima" da articulação (y)
    for id_ponta in ponta_dedos:
        if hand_landmarks.landmark[id_ponta].y < hand_landmarks.landmark[id_ponta - 2].y:
            contador += 1
            
    return contador

print("Iniciando leitura da câmera... Pressione 'q' para sair.")

while True:
    sucesso, imagem = cap.read()
    if not sucesso:
        break

    # Converte BGR (padrão OpenCV) para RGB (padrão MediaPipe)
    imagem_rgb = cv2.cvtColor(imagem, cv2.COLOR_BGR2RGB)
    resultados = maos.process(imagem_rgb)

    dedos_levantados = 0

    if resultados.multi_hand_landmarks:
        for landmarks_mao in resultados.multi_hand_landmarks:
            # Desenha o esqueleto da mão na tela
            mp_desenho.draw_landmarks(imagem, landmarks_mao, mp_maos.HAND_CONNECTIONS)
            
            # Conta os dedos
            dedos_levantados = contar_dedos(landmarks_mao)

            # Envia para o Arduino/ESP32
            if esp32 and esp32.is_open:
                # Envia o número como string e quebra de linha (ex: "3\n")
                esp32.write(f"{dedos_levantados}\n".encode())

            # Mostra o número na tela
            cv2.putText(imagem, f'Dedos: {dedos_levantados}', (10, 70), 
                        cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)

    cv2.imshow("Manopla Luminosa - Visao", imagem)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
if esp32: esp32.close()
