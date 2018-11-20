#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
# VIM: let g:pyindent_open_paren=2 g:pyindent_continue=2
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 21 13:16:42 2018

@author: Chunghan, glemmon
"""


import pandas as pd
#import json
import numpy as np
import sys
import re

#======================== Set rolling window size ==================
#Starting from date 2016-01-01 will give you rolling correlation calculations up to 2018-09-01
#The earlier the start date, the larger the file size. It's around 500MB with 2016-01-01 as start date

#Extract user specification of rolling window size
assert len(sys.argv) <= 2
if len(sys.argv)==2:
    window_size = int(sys.argv[1])
else:
    window_size = 6
#=============================================================


#======================Define Functions ====================

def remove_duplicated_columns(df):
    """
    Remove duplicates based on combinations https://stackoverflow.com/questions/51182228/python-delete-duplicates-in-a-dataframe-based-on-two-columns-combinations
    Input: Pandas dataframe with two symptoms columns that resemble undirected edges (i.e. with both A,B and B,A)
    Output: Pandas dataframe with duplicates with duplicates in symptomts columns removed
    """
    sorted_df = pd.DataFrame(np.sort(df[['symptom', 'pair']].values, 1))
    return df[~sorted_df.duplicated()]
    

def generate_corr_df(data, window_size):
    """
    Calculate columns of correlation measures across time
    Input: Pandas Dataframe
    Output: Pandas DataFrame with added columns of correlation calculated on aggregate and rolling basis
            The rows are each keyword pair, separated by state
    """
    to_concat = []
    #Go through all columns and store them in dataframe to calculate correlation
    for s in data['state'].unique():
        
        #Cast dataframe so that each keywork is along the column
        segment_by_state=data[data['state']==s][['date','trend','symptom']].pivot_table(index=['date'], columns='symptom', values='trend')
        
        #Calculate contemporaneous correlation between each pair
        corr = segment_by_state.corr('pearson')#Must use this to calculate pairwise correlation correctly. np looks at rows
        corr_data = corr.reset_index(drop=False).melt(id_vars= ['symptom'], var_name= 'pair', value_name='aggregate')
        
        #Calculate rolling window correlation
        for i in range(len(segment_by_state.index)):
            start = max(i-window_size, 0)
            stop = min(i+window_size+1, len(segment_by_state.index)+1)
            window= segment_by_state.iloc[start:stop,:]
            window_corr= window.corr('pearson')
            window_corr = window_corr.reset_index(drop=False).melt(id_vars= ['symptom'], var_name= 'pair', value_name=segment_by_state.index[i][:-3])
            #Merge data with original dataframe
            corr_data = corr_data.merge(window_corr, on=['symptom', 'pair'], how='left')
    
        corr_data=remove_duplicated_columns(corr_data)
        corr_data['state'] = s
        to_concat.append(corr_data)
        print("Just finished data for State: "+s)

    #Combine state level data into final DataFrame
    return pd.concat(to_concat, axis=0).reset_index(drop=True)

#==========================================================


#======================== Process data ==================
try:
   data = pd.read_csv('data_extraction/combined.tsv')
except FileNotFoundError:
    raise FileNotFoundError("Make sure your working directory is 'disease-trends' and not in any subdirectory")
    

concat_data = generate_corr_df(data, window_size)
concat_data.to_csv('data_processing/corr_by_state.'+str(window_size)+'.csv', index=False)
#=======================================================


#===============IGNORE: Create disease mapping JSON data================

##Create JSON file that saves the mapping from symptom to an array of diseases
#raw_mapping = pd.read_csv('data_extraction/research/ncomms5212-s4.txt', sep='\t')[['MeSH Symptom Term', 'MeSH Disease Term','TFIDF score']]
#symptom_disease_mapping = defaultdict(list)
#for symp in raw_mapping['MeSH Symptom Term'].unique():
#    disease_list = list(raw_mapping[raw_mapping['MeSH Symptom Term'] == symp]['MeSH Disease Term'])
#    symptom_disease_mapping[symp].extend(disease_list)
#x=json.dumps(symptom_disease_mapping, indent=1)
#
##Writing JSON to file https://stackoverflow.com/questions/12309269/how-do-i-write-json-data-to-a-file
#with open('data_processing/symptom_disease_mapping.json', 'w') as f:
#    json.dump(symptom_disease_mapping, f)


#===========================================================

    
