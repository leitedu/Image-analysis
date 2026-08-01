# 🔬 Cellular Silica Absorption & Spatial Distribution Analysis Pipeline

![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)
![Execution](https://img.shields.io/badge/Execution-Fully_Runnable-success?style=for-the-badge)

An automated Computer Vision and Unsupervised Learning pipeline designed to measure and analyze the spatial absorption and cellular accumulation of silica nanoparticles across varying culture concentrations and cultivation timeframes.

This tool processes paired [**Phase Contrast**](https://www.microscopyu.com/techniques/phase-contrast/introduction-to-phase-contrast-microscopy) and [**Fluorescence**]([https://www.microscopyu.com/techniques/phase-contrast/introduction-to-phase-contrast-microscopy](https://www.microscopyu.com/techniques/fluorescence/introduction-to-fluorescence-microscopy)) microscopy images, compares them against blank control media, applies [**ITU-R BT.601-7**](https://www.itu.int/dms_pubrec/itu-r/rec/bt/R-REC-BT.601-7-201103-I!!PDF-E.pdf) conversion to model differential brightness, and clusters high-concentration absorption zones using [**DBSCAN**](https://www.cis.lmu.de/~stef/seminare/klassifikation_2024/density_clustering.pdf) for statistical spatial profiling.


## 📌 Analytical Methodology & Physical Modeling

To understand whether silica is effectively absorbed by the cells and map its spatial distribution, the pipeline executes a sequence of matrix operations and clustering algorithms:

1. **Paired Image Processing:** The script ingests two sets of images:
   * **Cell Culture:** Paired Phase Contrast and Fluorescence images taken sequentially. The pipeline automatically distinguishes between the two techniques based on RGB channel magnitudes.
   * **Control Media:** Images of the culture media at the exact same concentration and time, but without cells, acting as a baseline.
2. **Differential Absorption Extraction:** The net absorption is modeled by subtracting the average baseline control media ($\bar{I}_{media}$) from the cellular fluorescence image ($I_{cell}$). The script isolates the positive difference (representing silica absorbed by the cells):
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

## 🛠️ Pipeline Architecture & Folder Structure

The pipeline expects image datasets to be organized in paired experimental runs by Cultivation Time and Concentration:

```text
data_folder/
├── 📂 cells/
│   └── 📂 {time}/
│       └── 📂 {concentration}/
│           ├── image_01_phase.tif      # Phase contrast image
│           ├── image_01_fluo.tif       # Corresponding fluorescence image
│           └── ...
├── 📂 media/
│   └── 📂 {time}/
│       └── 📂 {concentration}/
│           ├── control_01.tif          # Blank culture media images
│           └── ...
└── 📂 Maps/                            # Generated output directory (created by the pipeline if note provided)
```

The pipeline is built modularly to ensure clean separation of concerns:

* main.py: Orchestrates global parameters (concentrations, incubation times, DBSCAN thresholds, and folder paths) and initializes execution.

* loop.py: Handles directory traversal, couples cell/control images, coordinates mathematical transformations, and generates output databases.

* image_processing.py: Contains core image processing utility functions:

* technique_identifier(): Distinguishes phase contrast from fluorescence images based on channel brightness.

* average_images(): Computes pixel-wise mean arrays across control media images.

* luma(): Applies ITU-R BT.601-7 coefficients to calculate spatial brightness maps.

* clusterization.py: Runs DBSCAN pixel-level clustering, assigns color palettes, isolates noise points, and updates statistical metrics.

* plot.py: Assembles comparison figures (Original, Subtract, Binary Mask, and Cluster Maps) saved directly under ./Maps/{time}/{concentration}/.

## 🧰 Tech Stack
* **OpenCV (cv2) & PIL:** Image reading, normalization, array conversion, and color thresholding.
* **scikit-learn (DBSCAN):** Density-based spatial clustering for bioaccumulation analysis.
* **Matplotlib:** Multi-panel spatial map visualization and color-palette rendering.
* **Pandas:** Structured statistical database generation and Excel exporting (openpyxl).
