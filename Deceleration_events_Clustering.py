#!/usr/bin/env python
# coding: utf-8

# Aim: Clustering using Kmens Method and Visualizing the clustered data od deceleration events.

# Important Libariries which are used
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from statistics import mean
import random
from sklearn_pandas import DataFrameMapper
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler
from mpl_toolkits.mplot3d import Axes3D

# Input dec csv file from the current folder
data=pd.read_csv('final_deceleration_mavg-co.csv',index_col=0)

# Removing the parameters which are not used for clustering
traindf=data.drop(['LA array','FileName','V2','T1','T2','D2-D1','Avg LA','yaw array','mavg_jerk'],axis=1)

# Conversion formula is a*x+b where x is the parameter after scaling
a=traindf.max(axis=0)-traindf.min(axis=0)
b=traindf.min(axis=0)

# Scaling data using MInMaxScalar formula = X - Min / (Max-Min)
mapper1 = DataFrameMapper([(traindf.columns,MinMaxScaler())])
scaled_features = mapper1.fit_transform(traindf.copy(), 4)
scnum_train = pd.DataFrame(scaled_features, index=traindf.index, columns=traindf.columns)
#scnum_train.describe()


# Elbow Method for finding optimal number of clusters.
# taking average of WCSS for 15 random seed values for every cluster 

wcss_avg=[]

for i in range(1, 15):
    wcss_k=[]
    for j in range(1,11):
        km = KMeans(n_clusters = i, init = 'k-means++', max_iter = 300, n_init = 10, random_state = random.randint(0, 1000))
        km.fit(scnum_train)
        wcss_k.append(km.inertia_)
    wcss_avg.append(mean(wcss_k))
    
plt.plot(range(1, 15), wcss_avg)
plt.title('Random Seed ORC data', fontsize = 20)
plt.xlabel('No. of Clusters')
plt.ylabel('wcss')
plt.show()

# Performing Kmeans Clustering on the scaled data
km = KMeans(n_clusters = 6, init = 'k-means++', max_iter = 300, n_init = 10, random_state = 42)
y_means = km.fit_predict(scnum_train)

# Printing cluster centres of the clusters
centres=km.cluster_centers_
print('       C1,            C2,           C3,      C4,        C5,       C6')
print('V_b    {}'.format(centres[:,0]*a['V1']+b['V1']))
print('\u0394 V_b  {}'.format(centres[:,1]*a['V2-V1']+b['V2-V1']))
print('\u0394 T_b  {}'.format(centres[:,2]*a['T2-T1']+b['T2-T1']))
print('LA_min {}'.format(centres[:,3]*a['Min LA']+b['Min LA']))
print('Yr_b   {}'.format(centres[:,4]*a['yaw_rate']+b['yaw_rate']))


# Adding new columns for Clusters, Driver and Moving Avg Jerk
orig_data['Clusters']=y_means
orig_data['driver']=data['FileName'].copy()
orig_data['mavg_jerk']=data['mavg_jerk'].copy()
orig_data.tail()

# Renaming the Parameters for visualization
orig_data=traindf.rename(columns={"V1":"V_b","V2-V1": "\u0394 V_b","T2-T1":"\u0394 T_b","Min LA":"LA_min","yaw_rate":"Yr_b"})
sc_data=scnum_train.rename(columns={"V1":"V_b","V2-V1": "\u0394 V_b","T2-T1":"\u0394 T_b","Min LA":"LA_min","yaw_rate":"Yr_b"})

# Saving csv file into filename mentioned below
orig_data.to_csv('dec_clustered_mavg_jerk.csv')
scnum_train.to_csv('dec_scaled_data.csv')

# Ploting 3D scatter plot for 3 parameters mentioned below
plt.rcParams.update({'font.size': 16})
fig = plt.figure(figsize=(27,18))
ax = plt.axes(projection='3d')

# Taking different colours for different clusters
for g in np.unique(y_means):
    ix = np.where(y_means == g)
    ax.scatter3D(sc_data['V_b'].iloc[ix],sc_data['LA_min'].iloc[ix],sc_data['\u0394 V_b'].iloc[ix],label = g, marker='^')
ax.scatter3D(centres[:,0],centres[:,3],centres[:,1],c='black', s=200, alpha=1)

ax.set_xlim3d(0,max(sc_data['V_b']))
ax.set_ylim3d(0,max(sc_data['LA_min']))
ax.set_zlim3d(0,max(sc_data['\u0394 V_b']))

ax.set_xlabel('V_b', fontsize=24)
ax.set_ylabel('LA_min', fontsize=24)
ax.set_zlabel('\u0394 V_b', fontsize=24)
ax.legend()
plt.show()

# Plotting Boxplots for each parameters 
plt.figure(figsize=(30,5))
plt.rcParams.update({'font.size': 16})
plt.subplot(151)
sns.boxplot(x=y_means,y=orig_data['V_b'],data=orig_data)
plt.subplot(152)
sns.boxplot(x=y_means,y=abs(orig_data['\u0394 V_b']),data=orig_data)
plt.subplot(153)
sns.boxplot(x=y_means,y=orig_data['\u0394 T_b'],data=orig_data)
plt.subplot(154)
sns.boxplot(x=y_means,y=abs(orig_data['LA_min']),data=orig_data)
plt.subplot(155)
sns.boxplot(x=y_means,y=orig_data['Yr_b'],data=orig_data)

#sns.boxplot(x=y_means,y=orig_data['jerk'],data=orig_data)





