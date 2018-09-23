# -*- coding: utf-8 -*-
"""
Created on Fri Sep 21 13:16:42 2018

@author: Chunghan
"""


import pandas as pd
from collections import defaultdict
import json
import numpy as np

#======================== Set window size ==================
#Starting from date 2016-01-01 will give you rolling correlation calculations up to 2018-09-01
#The earlier the start date, the larger the file size. It's around 500MB with 2016-01-01 as start date
start_date= '2018-08-01'
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
    

def generate_corr_df(data, start_date = '2014-01-01'):
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
        corr_data = corr.reset_index(drop=False).melt(id_vars= ['symptom'], var_name= 'pair', value_name='aggregate_correlation')
        
        #Calculate rolling window correlation
        end_window = segment_by_state.index.get_loc(start_date)
        for i in range(end_window, segment_by_state.shape[0]):
            window= segment_by_state.iloc[i-end_window:i,:]
            window_corr= window.corr('pearson')
            window_corr = window_corr.reset_index(drop=False).melt(id_vars= ['symptom'], var_name= 'pair', value_name='Up to '+segment_by_state.index[i])
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
   data = pd.read_csv('../data_extraction/combined.csv')
except FileNotFoundError:
    raise FileNotFoundError("Make sure your working directory is disease-trends\/data_processing")
    

concat_data = generate_corr_df(data, start_date)
concat_data.to_csv('processed.csv', index=False)
#=======================================================


#===============Create disease mapping JSON data================

#Create JSON file that saves the mapping from symptom to an array of diseases
raw_mapping = pd.read_csv('../data_extraction/research/ncomms5212-s4.txt', sep='\t')[['MeSH Symptom Term', 'MeSH Disease Term','TFIDF score']]
symptom_disease_mapping = defaultdict(list)
for symp in raw_mapping['MeSH Symptom Term'].unique():
    disease_list = list(raw_mapping[raw_mapping['MeSH Symptom Term'] == symp]['MeSH Disease Term'])
    symptom_disease_mapping[symp].extend(disease_list)
x=json.dumps(symptom_disease_mapping, indent=1)

#Writing JSON to file https://stackoverflow.com/questions/12309269/how-do-i-write-json-data-to-a-file
with open('symptom_disease_mapping.json', 'w') as f:
    json.dump(symptom_disease_mapping, f)


#===========================================================




#=====================IGNORE: Obsolete functions=====================

#def calc_cross_cor(df,lead_symptom, lag_symptom ,lag=1):
#    """
#    Calculate lag n cross correlation
#    Input:  df Pandas Dataframe
#            symptoms String
#            lag Integer that shows the # periods the leading symptom leads the lagging sympton
#    Output: cross_correlation Float
#    """
#    lead_symptom = df[lead_symptom].shift(lag) #
#    return df[lag_symptom].corr(lead_symptom)    

#def merge_cross_corr(segment_by_state):
#    #Calculate cross correlation for each pair of key word series
#    cross_cor_list = []
#    for lead_sym in segment_by_state.columns:
#        for lag_sym in segment_by_state.columns:
#            #Calculate cross correlation https://stackoverflow.com/questions/33171413/cross-correlation-time-lag-correlation-with-pandas
#            cross_cor = calc_cross_cor(segment_by_state, lead_sym, lag_sym, 1)
#            cross_cor_list.append(pd.Series([lead_sym, lag_sym, cross_cor]))
#    lag1 = pd.concat(cross_cor_list,axis=1).T
#    return lag1
    

#    #Calculate cross correlation for each pair of keywords
#    lag1 = merge_cross_corr(segment_by_state)
#    #merge cross correlation and contemporaneous correlation data
#    corr_data = corr_data.merge(lag1, left_on=['symptom', 'pair'], right_on=[0,1], how='left').drop([0,1],axis=1).rename(columns={2:'cross correlation', 'symptom':'symptom_lead', 'pair':'symptom_lag'})
    