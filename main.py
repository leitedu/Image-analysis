from clusterization import clusterization
from config import culture_parameters, param_luma, folder, dbscan_parameters

#Define variables
hr = culture_parameters['time']
concentracoes = culture_parameters['concentration']

#Define variables
hr = culture_parameters['time']
concentracoes = culture_parameters['concentration']

if __name__ == "__main__":
  
  bd_clusters = {"Tempo de cultivo": [], "Concentração de sílica": [], "Imagem": [], "cluster": [], "n_pixels": [],
                            "soma_brilho": [], "max_brilho": [], "min_brilho": [], "media_brilho": []}

    for h in hr:
        for c in concentracoes:
            # Diretório onde as imagens estao localizadas
            path_cell = fr'{folder}\cells\{h}\{c}'
            path_media = fr'{folder}\media\{h}\sem celultivo-stokes\primeiro foco\{c}'

            # Média das imagens de meio de cultivo já convertida em array
            imagem_inicial_array, std_inicial_array = media_fotos(path_media)
            imagem_inicial = Image.fromarray(np.round(imagem_inicial_array).astype(np.uint8))
            
            # Fotos das células da pasta de uma determinada concentração e tempo de cultivo
            cell_files = os.listdir(path_cell)

            for image_cell in cell_files:
                
                # Verifica se imagem foi capturado por contraste de fase ou fluorescência
                flag = identifica_tecnica(fr'{path_cell}\{image_cell}')
                if flag == 0:
                    imagem_contraste = Image.open(fr'{path_cell}\{image_cell}')
                    continue
                
                # Gera array da diferena entre a imagem das células e do meio de cultivo
                imagem_celula_fluo = fr'{path_cell}\{image_cell}'
                imagem_final = Image.open(imagem_celula_fluo)
                imagem_final_array = np.array(imagem_final).astype(np.int16)

                img_dif = luma(imagem_final_array - imagem_inicial_array)

                param_cultivo = {'concentracao': c, 'tempo_cultivo': h}

                imagem_clusters, alpha_mask, dados_clusters_img, brilho_rgb, fig_cluster, n_clusters = clusterizar_imagem(img_dif)

                bd_clusters["Tempo de cultivo"] += [h for i in dados_clusters_img["cluster"]]
                bd_clusters["Concentração de sílica"] += [c for i in dados_clusters_img["cluster"]]
                bd_clusters["Imagem"] += [image_cell[:-4] for i in dados_clusters_img["cluster"]]

                for item, lista in dados_clusters_img.items():
                    bd_clusters[item] += lista

    df_clusters = pd.DataFrame(bd_clusters)
    df_clusters.to_excel(f'{folder}\cells\Base de dados Clusters.xlsx', index_label=False)
    
