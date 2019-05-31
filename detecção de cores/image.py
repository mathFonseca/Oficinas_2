#!/usr/bin/python
#-*- coding: utf-8 -*-
# IMPORTS

import numpy as np
import argparse
import cv2

#import os
#import commands
#from matplotlib import pyplot as plt

# DEFINES
end_imagem = 'img3.jpg'                  # Endereço da imagem


# LEMEBRE-SE: ORDEM INVERSA PARA O OPENCV
# color = [BLUE, GREEN, RED]

lower_blue = [20, 100, 100]
upper_blue = [30, 255, 255]

lower_red = [20, 100, 100]
upper_red = [30, 255, 255]
# O OpenCV lê na ordem BGR  (inverso de RGB). Nesse caso, a tupla tem que ser [B, G, R].
boundaries = [
    (lower_blue, upper_blue),  # LOWER blue. UPPER blue
    (lower_red, upper_red)  # LOWER red, UPPER red
]

# PRÉ SET PARA TIRAR A FOTO
quality = 30
height = 600
width = 800
nome = "img"
extensao = "png"

# PRÉ SET PARA FILTRO DE CINZA
binary_type = 0
binary_type_name = "Binarizacao Adaptativa: Gaussiana"
# Lista de Tipos e nomes: Seria legal criar uma enumeração para isso.
# 0 - Binarização simples
# 1 - Binarização de Otsu
# 2 - Binarização Adaptativa: Média
# 3 - Binarização Adaptativa: Gaussiana
save_flag = True
threshold_value = 127


# FUNCTIONS

# Se conecta ao raspberry para executar o comando necessario para tirar foto


def tirar_foto(qualidade, altura, largura, nome_foto, extensao_foto):
    string = "raspistill -q " + str(qualidade) + " -w " + str(largura) + " -h " + str(altura) + " -o " + nome_foto + "." + extensao_foto
    sucessful = 1
    sucessful = os.system(string)
    # demora para responder esse comando. Talvez seria interessante por um tempo limite?
    if(sucessful == 1):
        print("Nao foi possivel executar o comando de foto")
    elif(sucessful == 0):
        print("Foto tirada com sucesso")

# Carrega o arquivo de imagem na variável imagem.


def load_img(end_imagem):
    imagem = cv2.imread(end_imagem)
    return imagem

# Realiza uma escala de cinza através do OpenCV. Utiliza a variável imagem e retorna em img_cinza.

# NÃO ESTÁ CINZANDO A FOTO.


def escala_cinza(imagem, save_flag):
    img_cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
    #if save_flag == True:
        #cv2.imwrite('img_cinza.jpg', img_cinza)
    return img_cinza

# Realiza uma binarização. É necessário informar o tipo de binarização e um valor de threshold caso necessário.


def binarization(imagem, threshold_value, binary_type, save_flag):
    if binary_type == 0:
        ret, binary_img = cv2.threshold(imagem, threshold_value, 255, cv2.THRESH_BINARY)
        binary_img = cv2.subtract(255, binary_img) 
        if save_flag == True:
            cv2.imwrite('img_bin_normal.png', binary_img)
    elif binary_type == 1:
        ret, binary_img = cv2.threshold(imagem, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        if save_flag == True:
            cv2.imwrite('img_bin_otsu.png', binary_img)
    elif binary_type == 2:
        binary_img = cv2.adaptiveThreshold(imagem, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
        if save_flag == True:
            cv2.imwrite('img_bin_mean.png', binary_img)
    elif binary_type == 3:
        binary_img = cv2.adaptiveThreshold(imagem, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        if save_flag == True:
            cv2.imwrite('img_bin_gaussian.png', binary_img)

    return binary_img

# Realiza a plotagem de duas imagens: a imagem em escala de cinza e um gráfico (histograma) da mesma imagem.


def histograma(imagem):
    # ******************************
    # Histograma.
    plt.subplot(2, 1, 1), plt.imshow(imagem, cmap='gray')
    plt.title('Original'), plt.xticks([]), plt.yticks([])
    plt.subplot(2, 1, 2), plt.hist(imagem.ravel(), 256)
    plt.title('Histograma'), plt.xticks([]), plt.yticks([])
    plt.show()


def configure_cam():
    print("Preparando a camera...")
    print("Configuracoes pre-setadas:\nQualidade da camera: " + str(quality) + "\nAltura (em pixels): " + str(height) + "\nLargura (em pixels): " + str(width) + "\nNome do arquivo final: " + nome + "." + extensao + "")
    print("Para modificar as configuracoes, digite 1. Para continuar com essas configuracoes, digite 2.")
    option = input()
    if option == 1:
        print("Ainda nao implementado")
    elif option == 2:
        print("Configuracoes permanecem.")


def configure_filter():
    print("Preparando os filtros...")
    print("Configuracoes pre-setadas:\nTipo de binarizacao escolhida: " + binary_type_name + "\nThreshold Value: " + str(threshold_value) + "\nOpcao de salvamento automatico: " + str(save_flag))
    print("Para modificar as configuracoes, digite 1. Para continuar com essas configuracoes, digite 2.")
    option = input()
    if option == 1:
        print("Ainda nao implementado")
    elif option == 2:
        print("Configuraxoes permanecem")


def color_detection(imagem, save_flag):
    #args = vars(ap.parse_args())
    #imagem = cv2.imread(args[end_imagem])
    img = cv2.cvtColor(imagem, cv2.COLOR_BGR2HSV)
    #cv2.imwrite('img_brilhosa.png', img)
    lower = np.array([20, 100, 100], dtype="uint8")
    upper = np.array([30, 255, 255], dtype="uint8")

    mask = cv2.inRange(img, lower, upper)
    img_detected = cv2.bitwise_and(img, img, mask=mask)
    #if save_flag == True:
        #cv2.imwrite('img_color_detected.png', img_detected)

def erosion(imagem, save_flag):
    kernel = np.ones((2,2),np.uint8)
    erosion = cv2.erode(imagem,kernel,iterations = 60)
    if save_flag == True:
        cv2.imwrite('img_eroded.png', erosion)
    return(erosion)

def closing(imagem, save_flag):
    kernel = np.ones((5,5),np.uint8)
    closing = cv2.morphologyEx(imagem, cv2.MORPH_CLOSE, kernel)
    if save_flag == True:
        cv2.imwrite('img_closed.png', closing)
    return(closing)

def skeletonize(imagem, save_flag):
    imagem = imagem.copy()
    skel = imagem.copy()

    skel[:,:] = 0
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3,3))

    while True:
        eroded = cv2.morphologyEx(imagem, cv2.MORPH_ERODE, kernel)
        temp = cv2.morphologyEx(eroded, cv2.MORPH_DILATE, kernel)
        temp  = cv2.subtract(imagem, temp)
        skel = cv2.bitwise_or(skel, temp)
        imagem[:,:] = eroded[:,:]
        if cv2.countNonZero(imagem) == 0:
            break
    if save_flag == True:
        cv2.imwrite('img_skel.png', skel)
    return skel
# ******************************
# MAIN CODE

first_loop = True
main_loop = True

img = load_img(end_imagem)
print("Detectando cores...")
color_detection(img, save_flag)
print("Transformando imagem em escala de cinza... ")
img_cinza = escala_cinza(img, save_flag)
print("Binarizando imagem...")
bin_img = binarization(img_cinza, threshold_value, binary_type, save_flag)
print("Fazendo umas media...")
clo_img = closing(bin_img, save_flag)
print("Erodindo a imagem...")
ero_img = erosion(clo_img, save_flag)
print("Esqueletando a imagem...")
skel_img = skeletonize(ero_img, save_flag)