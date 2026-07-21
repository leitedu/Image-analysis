import os
import re
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

hr = ['24h', '48h']
concentracoes = ['04.5', '09.0', '18.0', '25.0', '32.0']
canais = ['red', 'green', 'blue']
diretorio = r'C:\Users\USER\Dropbox\2024-IC-Espectroscopia-Eduardo\FotosMicroscopio\SiO2\Imagenes de fluorescencia'

def identifica_tecnica(imagem):
    verifica = Image.open(imagem)
    verifica_np = np.array(verifica).astype(np.int16)
    media = np.average(verifica_np)
    if media < 50:
        return 1
    else:
        return 0

def mapas_de_cor1(caminho_imagem_inicial, nome_imagem_inicial, caminho_imagem_final, nome_imagem_final, parametros, canais):
    imagem_meio = fr'{caminho_imagem_inicial}\{nome_imagem_inicial}'
    imagem_celula_fluo = fr'{caminho_imagem_final}\{nome_imagem_final}'

    imagem_inicial = Image.open(imagem_meio)
    imagem_inicial_np = np.array(imagem_inicial).astype(np.int16)

    imagem_final = Image.open(imagem_celula_fluo)
    imagem_final_np = np.array(imagem_final).astype(np.int16)

    dif = (imagem_final_np - imagem_inicial_np)*5
    
    zeros = np.zeros((imagem_inicial_np.shape[0], imagem_inicial_np.shape[1], 3))
    canais_dif, array_plot = {}, {}

    for canal in canais:
        canais_dif[canal] = np.copy(zeros)
        canais_dif[canal][:, :, canais.index(canal)] = dif[:, :, canais.index(canal)]
        
        array_plot[canal] = np.copy(zeros)
        array_plot[canal][:, :, 0] = np.clip(-dif[:, :, canais.index(canal)], a_min=0, a_max=None)
        array_plot[canal][:, :, 1] = np.clip(dif[:, :, canais.index(canal)], a_min=0, a_max=None)

        figure, axis = plt.subplots(2, 2, figsize=(12, 8))
        axis[0, 0].imshow(imagem_inicial)
        axis[0, 1].imshow(imagem_final)
        axis[1, 0].imshow(array_plot[canal][:, :, 0], cmap='Reds', vmin=0, vmax=255)
        axis[1, 1].imshow(array_plot[canal][:, :, 1], cmap='Greens', vmin=0, vmax=255)

        axis[0, 0].set_title('Imagem inicio')
        axis[0, 1].set_title('Imagem fim')
        axis[1, 0].set_title('Variacao negativa')
        axis[1, 1].set_title('Variacao positiva')
        
        axis[0, 0].set_title(nome_imagem_inicial, fontweight='bold')
        axis[0, 1].set_title(nome_imagem_final, fontweight='bold')
        axis[1, 0].set_title('Variacao negativa', fontweight='bold')
        axis[1, 1].set_title('Variacao positiva', fontweight='bold')

        titulo = f'Mapa de cor Meio de cultivo x Celulas - {parametros['hora']} - {parametros['tempo cultivo']} mM - Canal {canal.capitalize()}'
        
        figure.suptitle(titulo, fontweight='bold', fontsize=13)
        plt.savefig(f'{diretorio}\cells\Mapas de cor\Mapa de cor {parametros['indice']+1} - {canal.capitalize()}.jpg', format='jpg', dpi=600)
