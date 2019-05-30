#!/usr/bin/python
#-*- coding: utf-8 -*-
# IMPORTS

import numpy as np
import argparse
import cv2

import os
import commands
from matplotlib import pyplot as plt

# DEFINES
end_imagem = 'image.jpg'                  # Endereço da imagem

#

lower_blue = [80, 65, 0]
upper_blue = [255, 255, 125]

lower_red = [0, 50, 50]
upper_red = [10, 255, 255]

# O OpenCV lê na ordem BGR  (inverso de RGB).
# Nesse caso, a tupla tem que ser [B, G, R].


# PRÉ SET PARA TIRAR A FOTO
quality = 30
height = 600
width = 800
nome = "img"
extensao = "png"

# PRÉ SET PARA FILTRO DE CINZA

binary_type = 0
binary_type_name = "Binarização Adaptativa: Gaussiana"

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
    string = ("raspistill -q "
              + str(qualidade)
              + " -w "
                + str(largura)
                + " -h "
                + str(altura)
                + " -o "
                + nome_foto
                + "."
                + extensao_foto)
    sucessful = 1
    sucessful = os.system(string)

    # Demora para responder esse comando.
    # Talvez seria interessante por um tempo limite?

    if(sucessful == 1):
        print("Nao foi possivel executar o comando de foto")
    elif(sucessful == 0):
        print("Foto tirada com sucesso")

# Carrega o arquivo de imagem na variável imagem.


def load_img(end_imagem):
    imagem = cv2.imread(end_imagem)
    return imagem

# Realiza uma escala de cinza através do OpenCV. Utiliza a variável imagem e retorna em img_cinza.


def escala_cinza(imagem, save_flag):
    img_cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
    if save_flag == True:
        cv2.imwrite('img_cinza.jpg', img_cinza)
    return img_cinza

# Realiza uma binarização. É necessário informar o tipo de binarização e um valor de threshold caso necessário.


def binarization(imagem, threshold_value, binary_type, save_flag):
    if binary_type == 0:
        ret, binary_img = cv2.threshold(imagem, threshold_value, 255, cv2.THRESH_BINARY)
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
    print("Preparando a câmera...")
    print("Configurações pré-setadas:\nQualidade da câmera: " + str(quality) + "\nAltura (em pixels): " + str(height) + "\nLargura (em pixels): " + str(width) + "\nNome do arquivo final: " + nome + "." + extensao + "")
    print("Para modificar as configurações, digite 1. Para continuar com essas configurações, digite 2.")
    option = input()
    if option == 1:
        print("Ainda não implementado")
    elif option == 2:
        print("Configurações permanecem.")


def configure_filter():
    print("Preparando os filtros...")
    print("Configurações pré-setadas:\nTipo de binarização escolhida: " + binary_type_name + "\nThreshold Value: " + str(threshold_value) + "\nOpção de salvamento automático: " + str(save_flag))
    print("Para modificar as configurações, digite 1. Para continuar com essas configurações, digite 2.")
    option = input()
    if option == 1:
        print("Ainda não implementado")
    elif option == 2:
        print("Configurações permanecem")


def blue_detection(imagem, save_flag, lower_blue, upper_blue):
    lower = np.array(lower_blue, dtype="uint8")
    upper = np.array(upper_blue, dtype="uint8")
    mask = cv2.inRange(imagem, lower, upper)
    img = cv2.bitwise_and(imagem, imagem, mask=mask)
    if save_flag == True:
        cv2.imwrite('img_blue.png', img)

    return img


def red_detection(imagem, save_flag, lower_red, upper_red):
    img_hsv = cv2.cvtColor(imagem, cv2.COLOR_BGR2HSV)
    lower = np.array(lower_red)
    upper = np.array(upper_red)

    mask_0 = cv2.inRange(img_hsv, lower, upper)

    output = img_hsv.copy()
    output[np.where(mask_0 == 0)] = 0

    if save_flag == True:
        cv2.imwrite('img_red.png', output)

    return output


def find_something(imagem):
    altura, largura = imagem.shape

    nao_preto = [1, 1]
    nao_preto[0] = -1
    nao_preto[1] = -1
    primeiro = None

    for linha in range(0, altura):
        for coluna in range(0, largura):

            if imagem[linha][coluna] != 0:

                nao_preto[0] = linha
                nao_preto[1] = coluna

                if(primeiro != None):

                    if linha < primeiro[0]:

                        primeiro[0] = linha

                    if coluna < primeiro[1]:

                        primeiro[1] = coluna
                else:

                    primeiro = nao_preto

    return primeiro

# ******************************
# MAIN CODE


print("Configurações atuais")

imagem = load_img(end_imagem)

blue_img = blue_detection(imagem, save_flag, lower_blue, upper_blue)

red_img = red_detection(imagem, True, lower_red, upper_red)

red_img_cinza = escala_cinza(red_img, True)

blue_img_cinza = escala_cinza(blue_img, True)

somewhat = find_something(blue_img_cinza)
somewhat2 = find_something(red_img_cinza)

print(somewhat2)

imagem[somewhat2[0], somewhat2[1]] = (0, 0, 0)
cv2.imwrite("teste.png", imagem)

# firstest_blue = find_something(blue_img)


'''
first_loop = True
main_loop = True

while main_loop:
    print("Iniciando código principal...")
    while first_loop:
        print("Bem vindo ao menu de câmera: ")
        print("Aperte 1 para tirar uma foto. ")
        print("Ou aperte qualquer outra tecla para sair.")
        # Melhorar esse menu
        option = input()
        if option == 1:
            configure_cam()
            tirar_foto(quality, height, width, nome, extensao)
            configure_filter()
            print("Iniciando processos... ")
            print("Carregando imagem...")
            img = load_img(end_imagem)
            print("Detectando cores...")
            blue_detection(img, save_flag, lower_blue, upper_blue)
            red_detection(img, save_flag, lower_red, upper_red)
            print("Transformando imagem em escala de cinza... ")
            img_cinza = escala_cinza(img, save_flag)
            print("Binarizando imagem...")
            bin_img = binarization(img_cinza, threshold_value, binary_type, save_flag)
        else:
            first_loop = False
            main_loop = False
'''
