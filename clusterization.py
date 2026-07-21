import cv2
import numpy as np
from sklearn.cluster import DBSCAN
import matplotlib.pyplot as plt

def clusterization(img_brilho: np.ndarray, limiar_brilho: int = 0.15, eps: float = 4, min_samples: int = 20):
    
    # Normalizar para 0-255
    brilho_rgb = cv2.normalize(img_brilho, None, 0, 1, cv2.NORM_MINMAX)
    
    # Aplicar limiar de brilho
    _, binary_mask = cv2.threshold(brilho_rgb, limiar_brilho, 1, cv2.THRESH_BINARY)
    
    # Obter coordenadas dos pontos relevantes
    pontos = np.column_stack(np.where(binary_mask > 0))  # (y, x)
    
    # Aplicar DBSCAN
    dbscan = DBSCAN(eps=eps, min_samples=min_samples)
    rotulos = dbscan.fit_predict(pontos)
    
    # Criar imagem clusterizada em RGB
    imagem_clusterizada = np.zeros((*img_brilho.shape, 3), dtype=np.uint8)
    
    # Número de clusters (excluindo ruído -1)
    clusters_unicos = set(rotulos) - {-1}
    n_clusters = len(clusters_unicos)
    
    # Gerar paleta de cores fixa para reprodutibilidade
    cmap = plt.cm.get_cmap("tab20", n_clusters)
    cores = (cmap(np.arange(n_clusters))[:, :3] * 255).astype(np.uint8)
    
    # Pintar os clusters
    for (y, x), label in zip(pontos, rotulos):
        if label == -1:  # pontos de ruído
            imagem_clusterizada[y, x] = (0, 0, 255)  # vermelho
        else:
            imagem_clusterizada[y, x] = cores[label % n_clusters]
    
    # Criar lista de resultados por cluster
    dados_clusters = {"cluster": [], "n_pixels": [], "soma_brilho": [], "max_brilho": [], "min_brilho": [], "media_brilho": []}

    for c in clusters_unicos:
        coords = pontos[rotulos == c]
        valores = img_brilho[coords[:, 0], coords[:, 1]]
        dados_clusters["cluster"].append(c)
        dados_clusters["n_pixels"].append(len(valores))
        dados_clusters["soma_brilho"].append(int(valores.sum()))
        dados_clusters["max_brilho"].append(int(valores.max()))
        dados_clusters["min_brilho"].append(int(valores.min()))
        dados_clusters["media_brilho"].append(float(valores.mean()))
    
    # Plotar comparação
    fig_cluster, axs = plt.subplots(1, 2, figsize=(10, 5))
    axs[0].imshow(img_brilho, cmap="gray")
    axs[0].set_title("Imagem de brilho acromático", fontweight='bold')
    axs[0].axis("off")
    
    axs[1].imshow(imagem_clusterizada)
    axs[1].set_title("Clusterização", fontweight='bold')
    axs[1].axis("off")
    # Texto com a quantidade de clusters
    axs[1].text(0.57, -0.06, f"Número de clusters: {n_clusters}", transform=axs[1].transAxes, ha="left", va="bottom", fontsize=9, color="black")
    
    return imagem_clusterizada, binary_mask, dados_clusters, brilho_rgb, fig_cluster, n_clusters
