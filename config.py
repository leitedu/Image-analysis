#Cell cultures parameters
culture_parameters = {
                        time: ['24h', '48h'], #cultivation time
                        concentration : ['04.5', '09.0', '18.0', '25.0', '32.0'] #silica concentration [mM]
                      }
#Luma
param_luma = [0.299, 0.587, 0.114]

#DBSCAN
dbsca_parameters = {
                        dblimiar: 50, #cultivation time
                        eps : 5,
                        min_samples : 20 #silica concentration [mM]
                      }

folder = r'./images' #folder of image cultures
