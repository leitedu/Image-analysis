import cv2
import numpy as np
from sklearn.cluster import DBSCAN
import matplotlib.pyplot as plt

def clusterizar_imagem(imagem: np.ndarray, limiar_brilho: int = 150, eps: float = 10, min_samples: int = 5):
    """
    Aplica DBSCAN em uma imagem para identificar clusters baseados no brilho e gera uma imagem com os clusters.
    
    Parâmetros:
    - imagem: ndarray representando a imagem em escala de cinza.
    - limiar_brilho: valor de brilho mínimo para filtrar os pixels (default: 150).
    - eps: parâmetro do DBSCAN que define a distância máxima para considerar pontos no mesmo cluster.
    - min_samples: número mínimo de pontos necessários para formar um cluster.

    Retorna:
    - imagem_clusterizada: imagem com os clusters pintados e os pontos fora dos clusters em azul.
    """
    # Aplicar limiar de brilho para filtrar os pontos relevantes
    threshold_value = 220
    _, binary_mask = cv2.threshold(imagem, limiar_brilho, 255, cv2.THRESH_BINARY)
    
    # Obter as coordenadas dos pontos filtrados
    pontos = np.column_stack(np.where(binary_mask > 0))  # Posições dos pixels com brilho maior que o limiar
    
    # Aplicar DBSCAN
    dbscan = DBSCAN(eps=eps, min_samples=min_samples)
    rotulos = dbscan.fit_predict(pontos)

    # Criar a imagem com os clusters
    imagem_clusterizada = np.copy(imagem)
    for i, ponto in enumerate(pontos):
        y, x = ponto
        if rotulos[i] == -1:  # Pontos fora de clusters (ruído)
            imagem_clusterizada[y, x] = 255  # Pintar de branco (ou azul para visualização colorida)
        else:
            imagem_clusterizada[y, x] = rotulos[i] * 15  # Usar o rótulo do cluster para colorir (multiplicar por 15 para visibilidade)

    # Criar a imagem de saída com pontos fora dos clusters em azul
    imagem_final = np.dstack([imagem_clusterizada, np.zeros_like(imagem_clusterizada), np.zeros_like(imagem_clusterizada)])
    imagem_final[binary_mask == 255] = [0, 0, 255]  # Pintar os pontos de ruído de azul (fora dos clusters)

    # Gerar o gráfico comparativo entre a imagem original e a imagem com clusters
    plt.figure(figsize=(12, 6))

    # Imagem original
    plt.subplot(1, 2, 1)
    plt.imshow(imagem, cmap='gray')
    plt.title("Imagem Original")
    plt.axis('off')

    # Imagem com clusters
    plt.subplot(1, 2, 2)
    plt.imshow(imagem_final)
    plt.title("Imagem com Clusters")
    plt.axis('off')

    plt.tight_layout()
    plt.show()

    return imagem_clusterizada  # Retorna a imagem com clusters

# Exemplo de uso:
# Carregar uma imagem em escala de cinza
imagem = cv2.imread('sua_imagem.jpg', cv2.IMREAD_GRAYSCALE)

# Aplicar a função para clusterização
imagem_clusterizada = clusterizar_imagem(imagem, limiar_brilho=150, eps=10, min_samples=5)
