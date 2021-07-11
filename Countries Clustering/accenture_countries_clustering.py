# -*- coding: utf-8 -*-
"""accenture_countries_clustering.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1nWn-sikghB7vYb26a8-EJbJ46WbK5SZ-
"""

import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn import preprocessing
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import numpy as np
import matplotlib.pyplot as plt
from sklearn import metrics
from scipy.spatial.distance import cdist
import plotly.express as px
import plotly
import plotly.io as pio

data=pd.read_csv("country_wise_latest.csv")

data= data.dropna(axis = 0, how ='any') 
len(data)

X=data.drop(["Country/Region","WHO Region"],axis=1)
Country_Region=data["Country/Region"]
WHO_Region=data['WHO Region']

X.replace([np.inf, -np.inf], "0", inplace=True)

import seaborn as sns
corr = X.corr()
ax = sns.heatmap(
    corr, 
    vmin=-1, vmax=1, center=0,
    cmap=sns.diverging_palette(20, 220, n=200),
    square=True
)
ax.set_xticklabels(
    ax.get_xticklabels(),
    rotation=45,
    horizontalalignment='right'
);
plt.savefig("Correlation_matrix_1.png")

kmeans = KMeans(n_clusters = 7, init = 'k-means++', random_state = 4)
y_kmeans = kmeans.fit_predict(X)
data["clusters1"]=y_kmeans
fig = px.choropleth(data, locations='Country/Region', 
                    locationmode='country names', color="clusters1", 
                    hover_name='Country/Region', range_color=[0, 6],
                    hover_data=["clusters1"],
                    color_continuous_scale="deep", 
                    title='Communites')
plotly.offline.plot(fig, filename='Communities2.html')

X = StandardScaler().fit_transform(X)

pca = PCA(n_components=13)
principalComponents = pca.fit_transform(X)
principalDf = pd.DataFrame(data = principalComponents
             , columns = ['PC1', 'PC2', 'PC3', 'PC4', 'PC5', 'PC6', 'PC7', 'PC8','pc9','pc10','pc11','pc12','pc13'])

pca.explained_variance_ratio_
var1=np.cumsum(np.round(pca.explained_variance_ratio_, decimals=4)*100)
plt.savefig("Cumulative_Variance_total.png")

pca = PCA(n_components=9)
principalComponents = pca.fit_transform(X)
principalDf = pd.DataFrame(data = principalComponents
             , columns = ['PC1', 'PC2', 'PC3', 'PC4', 'PC5', 'PC6', 'PC7', 'PC8','PC9'])

pca.explained_variance_ratio_
var=np.cumsum(np.round(pca.explained_variance_ratio_, decimals=4)*100)
plt.plot(var)
plt.xlabel('')
plt.ylabel('Cumulative Variance')
plt.savefig("Cumulative_Variance.png")

import seaborn as sns

corr = principalDf.corr()
ax = sns.heatmap(
    corr, 
    vmin=-1, vmax=1, center=0,
    cmap=sns.diverging_palette(20, 220, n=200),
    square=True
)
ax.set_xticklabels(
    ax.get_xticklabels(),
    rotation=45,
    horizontalalignment='right'
);
plt.savefig("Correlation_matrix_2.png")

principalDf = preprocessing.normalize(principalDf)

distortions = []
inertias = []
mapping1 = {}
mapping2 = {}
K = range(1, 10)
 
for k in K:
    # Building and fitting the model
    kmeanModel = KMeans(n_clusters=k,init = 'k-means++', random_state = 4).fit(principalDf)
    kmeanModel.fit(principalDf)
 
    distortions.append(sum(np.min(cdist(principalDf, kmeanModel.cluster_centers_,
                                        'euclidean'), axis=1)) / principalDf.shape[0])
    inertias.append(kmeanModel.inertia_)
 
    mapping1[k] = sum(np.min(cdist(principalDf, kmeanModel.cluster_centers_,
                                   'euclidean'), axis=1)) / principalDf.shape[0]
    mapping2[k] = kmeanModel.inertia_

plt.plot(K, distortions, 'bx-')
plt.xlabel('Values of K')
plt.ylabel('Distortion')
plt.title('The Elbow Method using Distortion')
plt.savefig("Distortion.png")

plt.plot(K, inertias, 'bx-')
plt.xlabel('Values of K')
plt.ylabel('Inertia')
plt.title('The Elbow Method using Inertia')
plt.savefig("Inertia.png")

kmeans = KMeans(n_clusters = 7,init = 'k-means++', random_state = 4)
y_kmeans = kmeans.fit_predict(principalDf )
data["clusters"]=y_kmeans
fig = px.choropleth(data, locations='Country/Region', 
                    locationmode='country names', color="clusters", 
                    hover_name='Country/Region', range_color=[0, 6],
                    hover_data=["clusters"],
                    color_continuous_scale="deep", 
                    title='Communites')

plotly.offline.plot(fig, filename='Communities1.html')

