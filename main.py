from loop import loop
from pathlib import Path

# Cells culture parameters
cultivation_times = ['24h'] # Example based on provided sample data
concentartions = ['09.0'] # Example based on provided sample data

# Luma parameters
param_luma = [0.299, 0.587, 0.114]

# DBSCAN parameters
limiar = 0.15
eps = 4
min_samples = 20

# Images folder
folder = r'./' #example

if __name__ == '__main__':

    folder_path = Path(folder)

    loop(main_db, cultivation_times, concentartions, folder_path, param_luma, limiar, eps, min_samples)
