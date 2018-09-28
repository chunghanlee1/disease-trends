# -*- coding: utf-8 -*-
"""
Created on Fri Sep 21 18:51:03 2018

@author: Chunghan
"""


import pandas as pd
import numpy as np
from scipy.spatial.distance import squareform
from scipy.cluster.hierarchy import linkage, fcluster
pd.set_option('display.max_columns',100)

try:
    data = pd.read_csv('data_processing/processed.csv')
except FileNotFoundError:
    raise FileNotFoundError("Make sure your working directory is 'disease-trends' and not in any subdirectory")
  
label_df_list = []
for st in data['state'].unique():
    #Merge empty dataframe https://stackoverflow.com/questions/28822011/merging-with-empty-dataframe
    state_data =  data[data['state']==st]
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
        label_df['state']=st
    label_df_list.append(label_df)
final_label_df = pd.concat(label_df_list, axis=0)[['symptom', 'state', 'Up to 2018-08-01', 'Up to 2018-09-01','aggregate_correlation']]


#Create final df that contains both cluster labels and pairwise correlation
final_merged_df = data.merge(final_label_df, on = ['symptom','state'], how='left', suffixes=('','_label')).merge(final_label_df, left_on = ['pair','state'], right_on = ['symptom','state'], how='left', suffixes=('','_label_pair')).drop(['symptom_label_pair'],axis=1)
to_concat=[]
#Check which pairs are in the same cluster for each of the periods and states
for col in final_label_df.columns.difference(['symptom', 'state']):
    #Filter for same cluster and omit duplicates
    cluster_members = final_merged_df[col+'_label'] == final_merged_df[col+'_label_pair']
    dup= final_merged_df['symptom'] != final_merged_df['pair']
    filtered_df=final_merged_df[['symptom', 'pair' ,'state',col+'_label',col]][(cluster_members&dup)].rename(columns={col:'corr', col+'_label': 'cluster'})
    #Melt the columns
    if 'aggregate' in col:
        filtered_df['period']= 'aggregate'
    else:
        filtered_df['period']= col[6:-3]
    to_concat.append(filtered_df.reset_index(drop=True))
final_merged_df = pd.concat(to_concat, axis=0)

final_merged_df.to_csv('data_analysis/clustered_keywords_by_state.csv', index=False)
