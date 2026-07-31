from loop import loop
from pathlib import Path

# Cells culture parameters
cultivation_times = ['24h']
concentartions = ['09.0']

# Luma parameters
param_luma = [0.299, 0.587, 0.114]

# DBSCAN parameters
limiar = 0.15
eps = 4
min_samples = 20

# Images folder
folder = r'./images'

# Cluster database dictionary
main_db = {
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

if __name__ == '__main__':

    folder_path = Path(folder)

    loop(main_db, cultivation_times, concentartions, folder_path, param_luma, limiar, eps, min_samples)
