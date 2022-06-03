# NOTE #
# BlackSpotAnalysis.py is to define the function to detect the Black Spot of traffic accident in New York City#
# This .py file is embedded in main.py #


import transbigdata as tbd
#tbd.set_mapboxtoken('pk.eyJ1IjoiamlheHVhbnciLCJhIjoiY2wxaTdxb2luMGJ1YzNsbGRjZTBraGQyNyJ9.bGnZXSnnTLwjhaeDSqxf_w')
import numpy as np
import os
import pandas as pd
from sklearn.cluster import DBSCAN
from collections import Counter
from sklearn. preprocessing import StandardScaler
import matplotlib.pyplot as plt
from pylab import rcParams
rcParams['figure.figsize']=5,5  #set figure parameters

# set path to save file that contains mapbox base map
#tbd.set_imgsavepath(r'C:\Users\cacy6\OneDrive - National University of Singapore\MUP_year2\y6s2\GE5219 spatial programming\project\code\\')

def blackspot(filename, datapath, output_path):
    """
    This is a function to detect black spot using the pre-defined parameters.

    :param filename: The file name of the data that is employed in black spot analysis.
    :param datapath: The path of data used.
    :param output_path: The path to save the result.
    :return: A png image that shows the result of black spot analysis.
    """
    # read csv file with geographical data
    data = pd.read_csv(filename)
    data['latitude'] = data['x']
    data['longitude'] = data['y']

    # Prepare data for model
    dbscan_data = data[['longitude','latitude']]
    dbscan_data = dbscan_data.values.astype('float32',copy=False)

    # Normalize data
    dbscan_data_scaler = StandardScaler().fit(dbscan_data)
    dbscan_data = dbscan_data_scaler.transform(dbscan_data)

    # Construct model
    # min_samples:: requires a minimum 20 data points in a neighborhood
    # eps:: in radius 0.02
    model = DBSCAN(eps = 0.002, min_samples = 150, metric='euclidean').fit(dbscan_data)

    # Separate outliers from clustered data
    outliers_df = data[model.labels_ == -1]
    clusters_df = data[model.labels_ != -1]

    colors = model.labels_
    colors_clusters = colors[colors != -1]
    color_outliers = ''

    # Get info about the clusters
    clusters = Counter(model.labels_)
    print(clusters)
    print(data[model.labels_ == -1].head())
    print('Number of clusters = {}'.format(len(clusters)-1))

    data['clusters'] = model.labels_

    bounds = [-74.308885,40.473596,-73.638552,40.944214]

    # Create a frame
    import matplotlib.pyplot as plt
    fig =plt.figure(1,(5,5),dpi=160)
    ax =plt.subplot(111)

    ax.scatter(clusters_df['longitude'], clusters_df["latitude"],
           c ='#000000', s=10)
    ax.set_xlabel('Longitude', family='Arial', fontsize=9)
    ax.set_ylabel('Latitude', family='Arial', fontsize=9)
    plt.sca(ax)

    tbd.plot_map(plt,bounds,zoom = 11,style = 1)

    tbd.plotscale(ax,bounds = bounds,textsize = 10,compasssize = 0.8, style = 2 , accuracy = 1300,rect = [0.06,0.9],zorder = 10)
    plt.axis('off')
    plt.xlim(bounds[0],bounds[2])
    plt.ylim(bounds[1],bounds[3])
    plt.title('Clustered NYC Traffic Crash by DBSCAN algorithm', family='Times New Roman', fontsize=12)

    # save the map to output_path
    fig.savefig(os.path.join(output_path, "blackspot.png"))




