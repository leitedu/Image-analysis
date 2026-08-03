import cv2
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN

def image_clustering(brightness_img: np.ndarray, brightness_limiar: int = 0.15, eps: float = 4, min_samples: int = 20):
    """
    Applies DBSCAN on an image to identify clusters based on brightness thresholding and generates a clustered image.
    
    Parameters:
    - brightness_img (np.ndarray): Grayscale input image matrix.
    - brightness_limiar (float): Minimum normalized brightness threshold (0.0 to 1.0) to filter pixels.
    - eps (float): DBSCAN parameter defining the maximum neighborhood distance for two points to be considered in the same cluster.
    - min_samples (int): Minimum number of pixels required to form a dense region (cluster).

    Returns:
    - clusterized_img (np.ndarray): RGB image (uint8) where pixels are color-coded by cluster ID, and noise is colored red.
    - binary_mask (np.ndarray): Binary mask image where values are 1 for pixels above the brightness threshold and 0 elsewhere.
    - unique_clusters (set): Set of unique cluster labels identified by DBSCAN (excluding noise label -1).
    - points (np.ndarray): Array of 2D coordinates (y, x) of all pixels that passed the threshold.
    - label (np.ndarray): Cluster label assignment for each point in 'points' (-1 represents noise).
    - rgb_brightness (np.ndarray): Normalized grayscale image with values scaled between 0.0 and 1.0.
    - n_clusters (int): Total count of valid clusters detected (excluding noise).
    """
    
    # Normalize to 0-255
    rgb_brightness = cv2.normalize(brightness_img, None, 0, 1, cv2.NORM_MINMAX)
    
    # Applies brightness threshold
    _, binary_mask = cv2.threshold(rgb_brightness, brightness_limiar, 1, cv2.THRESH_BINARY)
    
    # Threshold points array coordinates
    points = np.column_stack(np.where(binary_mask > 0))  # (y, x)
    
    # Applies DBSCAN
    dbscan = DBSCAN(eps=eps, min_samples=min_samples)
    labels = dbscan.fit_predict(points)
    
    # Generates RGB clusterized image
    clusterized_img = np.zeros((*brightness_img.shape, 3), dtype=np.uint8)
    
    # Number of clusters (excluding noise label -1)
    unique_clusters = set(labels) - {-1}
    n_clusters = len(unique_clusters)
    
    # Generates color map
    cmap = plt.colormaps["tab20"].resampled(n_clusters)
    cores = (cmap(np.arange(n_clusters))[:, :3] * 255).astype(np.uint8)
    
    # Clusters coloring
    for (y, x), label in zip(points, labels):
        if label == -1:  # points de ruído
            clusterized_img[y, x] = (0, 0, 255)  # vermelho
        else:
            clusterized_img[y, x] = cores[label % n_clusters]
    
    return clusterized_img, binary_mask, unique_clusters, points, labels, rgb_brightness, n_clusters

def db_update(unique_clusters, points, labels, brightness_img, image_cell, h, c):

    db_cluster = {
        "Cultivation time": [],
        "Silica concentration": [],
        "Image": [],
        "cluster": [],
        "n_pixels": [],
        "sum_brightness": [],
        "max_brightness": [],
        "min_brightness": [],
        "mean_brightness": [],
        }

    for item in unique_clusters:
        coords = points[labels == item]
        values = brightness_img[coords[:, 0], coords[:, 1]]
        db_cluster["cluster"].append(item)
        db_cluster["n_pixels"].append(len(values))
        db_cluster["sum_brightness"].append(int(values.sum()))
        db_cluster["max_brightness"].append(int(values.max()))
        db_cluster["min_brightness"].append(int(values.min()))
        db_cluster["mean_brightness"].append(float(values.mean()))

    db_cluster["Cultivation time"] = h
    db_cluster["Silica concentration"] = c
    db_cluster["Image"]= image_cell[:-4]

    return db_cluster
