import matplotlib.pyplot as plt

# Generates result map from orchestrator dictionary 
def plot_img(dic, culture_params, n_clusters, folder):

    map_fig, ax = plt.subplots(2, 2, figsize=(12, 8))

    for image, param_graph in dic.items():
        a, b = param_graph['subplot'][0], param_graph['subplot'][1]
        ax[a, b].imshow(param_graph['image'], cmap=param_graph['cmap'], alpha=param_graph['alpha'])
        ax[a, b].set_title(param_graph['title'], fontweight='bold')
        ax[a, b].set_axis_off()
        
    title = f'{dic["final_img"]["title"].capitalize()} Silica absortion map - Culture time {culture_params["cultivation_time"]} and Concentration {culture_params["concentration"]} mM'
    ax[1, 1].text(0.57, -0.06, f"Number of clusters: {n_clusters}", transform=ax[1, 1].transAxes, ha="left", va="bottom", fontsize=9, color="black")
    map_fig.suptitle(title, fontweight='bold', fontsize=13)

    map_fig.savefig(rf'{folder}\{culture_params["concentration"]} - {culture_params["cultivation_time"]} -  {dic["final_img"]["title"]}.jpg', format='jpg', dpi=1000)
    print(f'✅ Saving {culture_params["concentration"]} - {culture_params["cultivation_time"]} -  {dic["final_img"]["title"]}.jpg')

    # Clear the current axes.
    plt.cla() 
    # Clear the current figure.
    plt.clf() 
    # Closes all the figure windows.
    plt.close('all')    

# Elaborates orchestrator dictionary from results
def plot_dict(initial_img, final_img, image_cell, contrast_img, rgb_brightness, binary_mask, clusterized_img):
    dic = {'initial_img': {'image': initial_img, 'subplot': [0, 0], 'title': 'No culture media average', 'alpha': 1, 'cmap' : None},
                   'final_img': {'image': final_img, 'subplot': [0, 1], 'title': image_cell[:-4], 'alpha': 1, 'cmap' : None},
                   'contrat': {'image': contrast_img, 'subplot': [1, 0], 'title': 'Phase-contrast image', 'alpha': 0.8, 'cmap' : None},
                   'luma': {'image': rgb_brightness, 'subplot': [1, 0], 'title': 'Phase-contrast image + Absorption map', 'alpha': binary_mask, 'cmap' : 'Reds'},
                   'clusters': {'image': clusterized_img, 'subplot': [1, 1], 'title': 'Clusterization', 'alpha': 1, 'cmap' : None}
                   }

    return dic
