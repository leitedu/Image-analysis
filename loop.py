import os
import pandas as pd
from clusterization import image_clustering, db_update
from image_processing import read_image, technique_identifier, average_images, luma
from plot import plot_img, plot_dict


def loop(main_db, hr, concentrations, folder, param_luma, limiar, eps, min_samples):

    for h in hr:
        for c in concentrations:

            culture_params = {'concentration': c, 'cultivation_time': h}

            # Folders
            path_cell = folder / fr'cells/{h}/{c}'
            path_media = folder / fr'media/{h}/{c}'
            path_map =  folder / fr'Maps/{h}/{c}'

            path_map.mkdir(parents=True, exist_ok=True)

            # Takes average image from culture media at concentration c and cultivation_time h
            initial_img, initial_img_array = average_images(path_media) # returns image and correponding array
            
            # Cells images taken at concentration c and cultivation_time h (both phase-contrast and fluorescece)
            cell_files = os.listdir(path_cell)

            for image_cell in cell_files:
                
                # Verifies technique used in the picture
                flag = technique_identifier(path_cell / image_cell)
                if flag == 0: 
                    # If contrast-phase is identified, image is saved and script follows to fluorescence corresponding image
                    contrast_img, contrast_img_array = read_image(path_cell / image_cell)
                    continue
                
                # If fluorescence is identified, script takes it
                image_celula_fluo = path_cell / image_cell
                final_img, final_img_array = read_image(image_celula_fluo)

                # Takes difference between it and media average, in order to get absorted light
                img_dif = luma(final_img_array - initial_img_array, param_luma) # Clips just positive differences (absorption regions) and converts to brightness map

                # Runs clusterization algorithm (DBSCAN)
                clusterized_img, binary_mask, unique_clusters, points, labels, rgb_brightness, n_clusters = image_clustering(img_dif,  limiar, eps, min_samples)

                # Updates clusters database with clusters data found on image
                db_cluster = db_update(unique_clusters, points, labels, img_dif, image_cell, h, c)
                main_db.update(db_cluster)

                # Sets a support dictionary and structures result map from it
                dic = plot_dict(initial_img, final_img, image_cell, contrast_img, rgb_brightness, binary_mask, clusterized_img)
                plot_img(dic, culture_params, n_clusters, path_map)

    # Creates and save clusters database with Pandas
    df_clusters = pd.DataFrame(main_db)
    df_clusters.to_excel(folder / 'Clusters database.xlsx', index_label=False)
