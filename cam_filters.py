## Autores:
## Vitor Augusto Tibério - Eng. Elétrica 023 - EESC/USP

## Importando as Bibliotecas ## 
import cv2 as cv 
from PIL import Image as PIL_Image, ImageTk
from filters import * 
from tkinter import *

## Formatando o Vídeo ## 

video = cv.VideoCapture(0)
largura, altura = 600, 800
video.set(cv.CAP_PROP_FRAME_WIDTH, largura)
video.set(cv.CAP_PROP_FRAME_HEIGHT, altura)

## Definindo o "Aplicativo"

app = Tk()
app.title('Camera Mágica')
app.bind('<Escape>', lambda e: app.quit())
app.columnconfigure(0, weight = 3)
app.columnconfigure(1, weight = 1)

## Organização dos Filtros ## 

filter_selection = StringVar(app, "")

filtros = {
    "Original" : "",
    "Canny" : "canny",
    "Estilosa" : "stylish",
    "Invertida" : "inverter",
    "Binarizada" : "binarizacao",
    "Cinza" : "cinza"

}

legendas = Label(app)
legendas.grid(column= 0, row = 0, rowspan = 16, sticky= W, padx = 5, pady = 5)

i = 0
for (nome, valor) in filtros.items():
    Radiobutton(app, text=nome, variable=filter_selection, value = valor, indicator = 0).grid(column=1, row = i, sticky=NSEW)
    i = i + 1

def aplicar_filtro(img):
    if filter_selection.get() == 'canny':
        return canny(img, 100, 200)
    elif filter_selection.get() == 'stylish':
        return stylish(img)
    elif filter_selection.get() == 'inverter':
        return inverter(img)
    elif filter_selection.get() == 'binarizacao':
        img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        return binarizacao(img_gray)
    elif filter_selection.get() == 'cinza':
        return cinza(img)
    else:
        return img

def mostra_video():
    _, frame = video.read()
    imagem = aplicar_filtro(frame)
    imagem = cv.cvtColor(imagem, cv.COLOR_BGR2RGBA)
    img = PIL_Image.fromarray(imagem)
    photo_image = ImageTk.PhotoImage(image=img)
    legendas.photo_image = photo_image
    legendas.configure(image=photo_image)
    legendas.after(10, mostra_video)

app.after(100, mostra_video)
app.mainloop()