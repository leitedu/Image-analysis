# 🔬 Cellular Silica Absorption & Spatial Distribution Analysis Pipeline

![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)
![Execution](https://img.shields.io/badge/Execution-Fully_Runnable-success?style=for-the-badge)

An automated Computer Vision and Unsupervised Learning pipeline designed to measure and analyze the spatial absorption and cellular accumulation of silica nanoparticles across varying culture concentrations and cultivation timeframes.

This tool processes paired [**Phase Contrast**](https://www.microscopyu.com/techniques/phase-contrast/introduction-to-phase-contrast-microscopy) and [**Fluorescence**](https://www.microscopyu.com/techniques/fluorescence/introduction-to-fluorescence-microscopy) microscopy images, compares them against blank control media, applies [**ITU-R BT.601-7**](https://www.itu.int/dms_pubrec/itu-r/rec/bt/R-REC-BT.601-7-201103-I!!PDF-E.pdf) conversion to model differential brightness, and clusters high-concentration absorption zones using [**DBSCAN**](https://www.cis.lmu.de/~stef/seminare/klassifikation_2024/density_clustering.pdf) for statistical spatial profiling.


## 📌 Analytical Methodology & Physical Modeling

To understand whether silica is effectively absorbed by the cells and map its spatial distribution, the pipeline executes a sequence of matrix operations and clustering algorithms:

1. **Paired Image Processing:** The script ingests two sets of images:
   * **Cell Culture:** Paired Phase Contrast and Fluorescence images taken sequentially. The pipeline automatically distinguishes between the two techniques based on RGB channel magnitudes.
   * **Control Media:** Images of the culture media at the exact same concentration and time, but without cells, acting as a baseline.
2. **Differential Absorption Extraction:** The net absorption is modeled by subtracting the average baseline control media (<i>Ī</i><sub>media</sub>) from the cellular fluorescence image (<i>I</i><sub>cell</sub>). The script isolates the positive difference (representing silica absorbed by the cells):
   $$\Delta I = \max(0, I_{cell} - \bar{I}_{media})$$
3. **LUMA BT.601-7 Conversion:** To convert 3-channel RGB differential signal matrices into a standardized scalar brightness map $Y$ for clustering, we apply the ITU-R BT.601-7 luma coefficients:
   $$Y = 0.299 \cdot R + 0.587 \cdot G + 0.114 \cdot B$$
4. **Spatial Clustering (DBSCAN):** High-density absorption areas on the brightness map are extracted via adaptive thresholding and clustered using **DBSCAN** (Density-Based Spatial Clustering of Applications with Noise). This separates true silica uptake zones from diffuse background noise and maps the spatial distribution.
5. **Database Generation:** The spatial properties of each cluster are calculated and appended to a statistical database for further analysis.

```text
[Phase Contrast + Fluorescence Pair] ──┐
                                       ├─────> [Isolate Fluorescence] ─────────> [Subtract Control Media]
[Control Media Images (No Cells)]   ───┘                                                     │
                                                                                             ▼
[Excel Database + Result Maps] <── [DBSCAN Metrics] <── [Spatial Clustering] <── [Brightness Conversion (luma)]
```

## 🛠️ Repository Structure & Workflow

To ensure the automated batch processing works correctly, the raw images must be placed in a specific hierarchical folder structure (`{time}/{concentration}/`). 

Below is the expected project directory layout:

```text
.
├── 📂 cells/                       # Raw experimental cell images (Phase Contrast & Fluorescence)
│   └── 📂 24h/                     # └── Folder grouped by cultivation time (e.g., 24h, 48h)
│       └── 📂 09.0/                #     └── Folder grouped by concentration (e.g., 09.0)
│           ├── 📄 image0030.bmp 
│           └── 📄 image0031.bmp
│
├── 📂 media/                       # Control baseline images (without cells)
│   └── 📂 24h/                     # └── Must match the exact time/concentration hierarchy
│       └── 📂 09.0/           
│           ├── 📄 image0006.bmp
│           └── 📄 image0007.bmp
│
├── 📂 outputs/                     # Auto-generated pipeline results
│   ├── 🖼️ 24h image0031.jpg        # Multi-panel result map with clustered zones
│   └── 📊 Clusters database.xlsx   # Consolidated statistical cluster data
│
├── ⚙️ Pipeline Scripts
│   ├── main.py                      # 🚀 Entry point: Define hyperparameters and run the pipeline
│   ├── loop.py                      # Orchestrates the batch processing across all folders
│   ├── image_processing.py          # Handles image I/O, technique auto-detection, and LUMA conversion
│   ├── clusterization.py            # Core DBSCAN algorithm and database update logic
│   └── plot.py                      # Generates and saves the result output maps
│
├── 📄 requirements.txt             # Python dependencies
├── 📄 LICENSE                      # Open-source MIT License
└── 📄 README.md                    # Project documentation
````

## 🗂️ Core Components Explained
* `cells/` & `media/` (The Inputs): The raw image directories. The pipeline relies on this rigid `{time}/{concentration}` folder structure to accurately pair the experimental cells with their respective baseline control media. Images are typically `.bmp` or `.tif` files.

* `outputs/` (The Outputs): Automatically generated by the pipeline. It stores the visual diagnostic maps (showing the spatial distribution of the absorbed silica) and the final Excel database containing the statistical properties of every identified cluster.

* `main.py` (Execution): This is the only file you need to run. It holds the global configurations, such as LUMA coefficients, DBSCAN hyperparameters (`eps`, `min_samples`), and the root folder path.

## 🧰 Tech Stack
* **OpenCV (cv2) & PIL:** Image reading, normalization, array conversion, and color thresholding.
* **scikit-learn (DBSCAN):** Density-based spatial clustering for bioaccumulation analysis.
* **Matplotlib:** Multi-panel spatial map visualization and color-palette rendering.
* **Pandas:** Structured statistical database generation and Excel exporting (openpyxl).
