## Autore: Vitor Augusto Tibério - Eng. Elétrica 023 - Automação 

## Dependências para o programa: 
# pip install cvzone 
# pip instal midiapipe

## Importando as bibliotecas ## 
from cvzone.HandTrackingModule import HandDetector
import cv2 as cv

## Código para abrir o vídeo ## 

vid = cv.VideoCapture(0, cv.CAP_DSHOW)
vid.set(3, 1280)
vid.set(4, 720)


detector = HandDetector()
desenho = []

while True: 
    check, img = vid.read()
    maos = detector.findHands(img, draw=True)
    mao = maos[0]
    if mao: 
        lmlist = mao[0]['lmList']
        dedos = detector.fingersUp(mao[0])
        dedos_up = dedos.count(1)
        print(f'Você está com {dedos_up} dedos levantados')
        if dedos_up == 1:
            x,y = lmlist[8][0], lmlist[8][1]
            cv.circle(img, center=(x,y), radius= 15, color=(255, 0,0), thickness= -1) 
            desenho.append((x,y))
        elif dedos_up != 1 and dedos_up != 3:
            desenho.append((0,0))
        elif dedos_up ==3: 
            desenho = []
        
        for id, ponto in enumerate(desenho):
            x,y = ponto[0], ponto[1]
            cv.circle(img, center=(x,y), radius= 10, color=(255, 0,0), thickness= -1) 
            
    img_flip = cv.flip(img, 1)     
    cv.imshow('Lousa Magica', img_flip)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break 




