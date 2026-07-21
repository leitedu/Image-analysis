import os
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

def plot_img(dic, param_cultivo, n_clusters):
    fig_mapa, ax = plt.subplots(2, 2, figsize=(12, 8))

    for imagem, param_graph in dic.items():
        a, b = param_graph['subplot'][0], param_graph['subplot'][1]
        ax[a, b].imshow(param_graph['imagem'], cmap=param_graph['cmap'], alpha=param_graph['alpha'])
        ax[a, b].set_title(param_graph['titulo'], fontweight='bold')
        ax[a, b].set_axis_off()
        
    titulo = f'Mapa de absorção celular de sílica - Tempo de cultivo {param_cultivo["tempo_cultivo"]} e concentração {param_cultivo["concentracao"]} mM'
    ax[1, 1].text(0.57, -0.06, f"Número de clusters: {n_clusters}", transform=ax[1, 1].transAxes, ha="left", va="bottom", fontsize=9, color="black")
    fig_mapa.suptitle(titulo, fontweight='bold', fontsize=13)

    #plt.show()
    fig_mapa.savefig(f'{folder}\cells\Mapas\Mapas de absorcao\{param_cultivo["concentracao"]} - {param_cultivo["tempo_cultivo"]} -  {dic["imagem final"]["titulo"]}.jpg', format='jpg', dpi=1000)
    print(f'Salvando {param_cultivo["concentracao"]} - {param_cultivo["tempo_cultivo"]} -  {dic["imagem final"]["titulo"]}.jpg')

def identifica_tecnica(imagem):
    verifica = Image.open(imagem)
    verifica_array = np.array(verifica).astype(np.int16)
    media = np.average(verifica_array)
    if media < 50:
        return 1
    else:
        return 0

def media_fotos(endereco):
    arquivos = os.listdir(endereco)
    arrays = []

    for foto in arquivos:
        caminho_imagem = endereco + '\\' + foto
        imagem = Image.open(caminho_imagem)
        imagem_array = np.array(imagem).astype(np.int16)
        arrays.append(imagem_array)

    media = np.average(arrays, axis=0)
    std = np.std(arrays, axis=0)

    return media, std

def luma(imagem):           
    positivo = np.zeros((imagem.shape[0], imagem.shape[1]))
    for i in range(3):
        positivo[:, :] += param_luma[i]*np.clip(imagem[:, :, i], a_min=0, a_max=None)

    return positivo
