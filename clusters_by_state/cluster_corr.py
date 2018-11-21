#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
# VIM: let g:pyindent_open_paren=2 g:pyindent_continue=2
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 21 18:51:03 2018

@author: Chunghan, glemmon
"""


import pandas as pd
import numpy as np
import sys
from scipy.spatial.distance import squareform
from scipy.cluster.hierarchy import linkage, fcluster
pd.set_option('display.max_columns',100)

infile = sys.argv[1]
outfile = sys.argv[2]
try:
    data = pd.read_csv(infile)
except FileNotFoundError:
    raise FileNotFoundError("Make sure your working directory is 'disease-trends' and not in any subdirectory")

label_df_list = []
for st in data['state'].unique():
    #Merge empty dataframe https://stackoverflow.com/questions/28822011/merging-with-empty-dataframe
    state_data =  data[data['state']==st]
    try:
        for ind, col in enumerate(state_data.columns.difference(['symptom', 'pair','state'])):

            corr_data =state_data[['symptom','pair', col]].pivot_table(index=['symptom'], columns='pair', values=col).fillna(0)
            corr_data = corr_data+corr_data.T
            #Fill diagonal https://stackoverflow.com/questions/24475094/set-values-on-the-diagonal-of-pandas-dataframe
            np.fill_diagonal(corr_data.values, 1)
            #Replace data with floating point error
            corr_data = corr_data.mask((corr_data>1), np.round(corr_data.values))
            
            #Grouping correlation https://stackoverflow.com/questions/38070478/how-to-do-clustering-using-the-matrix-of-correlation-coefficients
            #Agglomerative clustering https://www.youtube.com/watch?v=XJ3194AmH40
            #We do not adopt 1-abs(corr) as suggested becuase we are interested in terms that are searched TOGETHER, which requires positive correlation
            X= 1-corr_data
            #Handle NaN values to make sure they don't belong in any cluster
            X= X.fillna(100)
            
            hierarchy = linkage(squareform(X), method='average')
            labels=fcluster(hierarchy, 0.7, criterion= 'distance')
            to_merge = pd.DataFrame({'symptom':corr_data.index, col:labels})
            if ind == 0:
                label_df = to_merge
            else:
                label_df = label_df.merge(to_merge, on='symptom')
            label_df['state']=st
        label_df_list.append(label_df)
    except:
        pass
    print('Finished calculating corr for '+st)
final_label_df = pd.concat(label_df_list, axis=0)



to_concat=[]
#Check which pairs are in the same cluster for each of the periods and states
for col in final_label_df.columns.difference(['symptom', 'state']):
    
    filtered_df=final_label_df[['symptom','state',col]].rename(columns={ col: 'cluster'})
    
    #Melt the columns
    if 'aggregate' in col:
        filtered_df['period']= 'aggregate'
    else:
        filtered_df['period']= col
    to_concat.append(filtered_df.reset_index(drop=True))
    
final_cluster_df = pd.concat(to_concat, axis=0)

#be aware of NA values, which should have all been separated out
final_cluster_df.to_csv(outfile, index=False)
