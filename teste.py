
import numpy as np

tupla = None

altura = 5
largura = 5

imagem = np.zeros((altura, largura))

for linha in range(0, altura):
    for coluna in range(0, largura):
        imagem[linha][coluna] = linha + coluna


tupla = [0, 0]

for linha in range(0, altura):
    for coluna in range(0, largura):
        tupla_temp = (linha, coluna)

        if linha > tupla[0]:
            print("eae")
        else:
            print("aaa")
