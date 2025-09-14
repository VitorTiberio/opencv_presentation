## Developed by: Vitor Augusto Tiberio and Felipe Maitan ## 

## Importing Packages ## 

import cv2 as cv
import numpy as np 
from scipy import interpolate
import matplotlib.pyplot as plt

## Defining functions ## 
def image_plot(image):
    plt.figure(figsize=(5,5))
    plt.imshow(image, cmap = 'gray', vin = 0, vmax = 255)
    plt.title('shape{}'.format(image.shape))
    plt.show()

def histogram_plot(image):
    plt.hist(image.flatten(),bins=100,density=False,range=(0,255))
    plt.xlim([0,255])
    plt.show()

def gaussian_filter(image, k = 9):
    gauss_img = cv.GaussianBlur(image, (k,k), 0 ,0)

    return gauss_img

def binarizacao(image):
    th_value, img_bin_otsu = cv.threshold(image, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)

    return img_bin_otsu 

def canny(image, thr1 = 100, thr2 = 200):
    canny = cv.Canny(image, thr1,  thr2)
    return canny

def stylish(image):
    img_blur = cv.GaussianBlur(image, (5,5), 0, 0)
    style = cv.stylization(img_blur, sigma_s= 8, sigma_r= 0.1)
    return style 

def inverter(image):
    inv = cv.bitwise_not(image)
    return inv 

def new_kernel(lenght):
    kernel = np.ones((lenght, lenght))/(lenght**2)
    return kernel

def increase_contrast(image):
    A = image.min()
    B = image.max()
    img_out = (image - A)*(255/(B-A))

    return img_out

    ## Main Code ##

if __name__ == "__main__":

    img = cv.imread('tiberio_family_1.jpeg')

    if img is None:
        print("Imagem não encontrada!")
    else:
        print('Imagem Carregada com Sucesso!')

    img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    cv.imwrite('images_with_filter/imagem_cinza.png', img_gray)

    img_gauss = gaussian_filter(img)
    cv.imwrite('images_with_filter/imagem_gauss.png', img_gauss)

    img_canny = canny(img_gray, 100, 160)
    cv.imwrite('images_with_filter/imagem_canny.png', img_canny)

    img_contrast = increase_contrast(img_gray)
    cv.imwrite('images_with_filter/imagem_aumento_contraste.png', img_contrast)

    img_bin = binarizacao(img_gray)
    cv.imwrite('images_with_filter/imagem_binarizacao.png', img_bin)

    img_style = stylish(img)
    cv.imwrite('images_with_filter/imagem_style.png', img_style)

    img_not = inverter(img)
    cv.imwrite('images_with_filter/imagem_not.png', img_not)

    filtro12 = new_kernel(12)
    g1 = cv.filter2D(img_gray, -1, filtro12)
    cv.imwrite('images_with_filter/imagem_kernel_ones.png', g1)

    print('Terminei o processamento das imagens! =)')