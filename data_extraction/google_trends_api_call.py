#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
# -*- coding: utf-8 -*-
"""
Created on Sat Sep  8 19:18:09 2018

@author: Chunghan
"""

import pandas as pd
from pytrends.request import TrendReq
import time
import numpy as np


#Initiate data & variables
states_list = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", 
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]

def parse_args():
    from argparse import ArgumentParser, FileType
    parser = ArgumentParser(description='Calculate p-values for pairs of terms')
    parser.add_argument(
        'symptoms',
        type=FileType('r'),
        help='Tab delimited file. First column is the symptom descriptor',
    )
    parser.add_argument(
        '--offset',
        type=int,
        default=0,
        help='Number of term in term list to start with',
    )
    parser.add_argument(
        '--nterms',
        type=int,
        default=500,
        help='Number of terms to process',
    )


    return parser.parse_args()

def main():
    args = parse_args()
    # Login to Google. Only need to run this once, the rest of requests will use the same session.
    pytrend = TrendReq()
    symptoms_list = [r.strip().split('\t')[0] for r in args.symptoms]
    symptoms_list = symptoms_list[offset+1:nterms+1]# add 1 for header
    raw_data={state:[] for state in states_list}
    n_symptoms=len(symptoms_list)
    start_index=0

    #Start collecting data. For each keyword...
    for index in range(start_index, n_symptoms,4):
        #If reach end of list
        if n_symptoms - index < 3:
            symptoms = symptoms_list[index:]
        #else we select 4 keywords at once
        else:
            symptoms=symptoms_list[index:index+4]
        
        #For each state, fetch data...
        for state in states_list:
            # Need to extract data relative to a baseline. Here we use "cough"
            pytrend.build_payload(kw_list=['cough']+symptoms, timeframe= 'all', geo='US-'+state)
            # Interest Over Time
            interest_over_time_df = pytrend.interest_over_time()
            raw_data[state].append(interest_over_time_df)
            print('Downloaded data for Symptom(s): {}, State: {}'.format(symptoms,state))
            time.sleep(np.random.randint(45,65))
    
    
    #If error occurs, run loop again with the start_index below
    start_index=index
    
    
    #Aggregate data by state
    data_aggregated_by_state=[]
    for state, data_list in raw_data.items():
        #If data is not empty, then we go ahead and record result
        if data_list:
            symptom_df_by_time_and_state = data_list[0]
            #If more than 1 result, then we merge the dataframes
            if len(data_list)>1:
                for df in data_list[1:]:
                    cols_to_keep = df.columns.difference(['isPartial','cough'])
                    symptom_df_by_time_and_state = pd.merge(symptom_df_by_time_and_state, df[cols_to_keep], how='inner',left_index=True, right_index=True)
                    symptom_df_by_time_and_state['state']=state
            else:    
                symptom_df_by_time_and_state['state']=state
            #Record data
            data_aggregated_by_state.append(symptom_df_by_time_and_state)
    
    
    #Check to make sure we can combine the data frame. If not, then we need to save each dataframe in the list separately
    if sum([not d.shape==data_aggregated_by_state[0].shape for d in data_aggregated_by_state]) == 0:
        final_df = pd.concat(data_aggregated_by_state, axis=0)
        final_df.to_csv('.'.join(['data',str(args.offset),'-',str(args.nterms-1), 'csv']), sep=',', encoding='utf-8')
    
if(__name__=='__main__'):
    main()
