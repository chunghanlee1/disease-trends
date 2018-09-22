# -*- coding: utf-8 -*-
"""
Created on Fri Sep 21 18:51:03 2018

@author: Chunghan
"""


import pandas as pd
import numpy as np
from scipy.spatial.distance import squareform
from scipy.cluster.hierarchy import linkage, fcluster

try:
    data = pd.read_csv('../data_processing/processed.csv')
except FileNotFoundError:
    raise FileNotFoundError("Make sure your working directory is disease-trends\/data_analysis")
  
    
#Merge empty dataframe https://stackoverflow.com/questions/28822011/merging-with-empty-dataframe
state_data =  data[data['state']=='AL']
for ind, col in enumerate(state_data.columns.difference(['symptom', 'pair','state'])):
    corr_data =state_data[['symptom','pair', col]].pivot_table(index=['symptom'], columns='pair', values=col).fillna(0)
    corr_data = corr_data+corr_data.T
    #Fill diagonal https://stackoverflow.com/questions/24475094/set-values-on-the-diagonal-of-pandas-dataframe
    np.fill_diagonal(corr_data.values, 1)
    
    #Grouping correlation https://stackoverflow.com/questions/38070478/how-to-do-clustering-using-the-matrix-of-correlation-coefficients
    #Agglomerative clustering https://www.youtube.com/watch?v=XJ3194AmH40
    #We do not adopt 1-abs(corr) as suggested becuase we are interested in terms that are searched TOGETHER, which requires positive correlation
    X= 1-corr_data
    hierarchy = linkage(squareform(X), method='average')
    labels=fcluster(hierarchy, 0.7, criterion= 'distance')
    to_merge = pd.DataFrame({'symptom':corr_data.index, col:labels})
    if ind == 0:
        label_df = to_merge
    else:
        label_df = label_df.merge(to_merge, on='symptom')
label_df
