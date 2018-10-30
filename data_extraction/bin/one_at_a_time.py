#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
# VIM: let g:pyindent_open_paren=2 g:pyindent_continue=2
# -*- coding: utf-8 -*-
"""
Created on Sat Sep  8 19:18:09 2018

@author: Chunghan
"""

import pandas as pd
from pytrends.request import TrendReq
from pytrends.exceptions import ResponseError
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
    parser.add_argument(
        '--out_prefix',
        default='data',
        help='Tab delimited file. First column is the symptom descriptor',
    )
    parser.add_argument(
        'symptoms',
        type=FileType('r'),
        help='Tab delimited file. First column is the symptom descriptor',
    )
    args = parser.parse_args()
    return args

def main():
    args = parse_args()
    # Login to Google. Only need to run this once, the rest of requests will use the same session.
    pytrend = TrendReq()
    symptoms_list = [r.strip().split('\t')[0] for r in args.symptoms]
    symptoms_list = symptoms_list[args.offset+1:args.offset+1+args.nterms]
    with open('parts/'+'.'.join([args.out_prefix, str(args.offset), str(args.offset+args.nterms-1),'tsv']), 'w') as fh:
        for symptom in symptoms_list:
            #For each state, fetch data...
            for state in states_list:
                # Need to extract data relative to a baseline. Here we use "cough"
                while True:
                    try:
                        pytrend.build_payload(kw_list=[symptom], timeframe= 'all', geo='US-'+state)
                        time.sleep(np.random.randint(45,65))
                        break
                    except:
                        print('Try again for {},{}'.format(state, symptom))
                        time.sleep(np.random.randint(45,65))
                        continue
                interest_over_time_df = pytrend.interest_over_time()
                interest_over_time_df['state']=state
                interest_over_time_df['symptom']=symptom
                interest_over_time_df.to_csv(fh, sep=',', encoding='utf-8')
                print('Downloaded data for State: {}, Symptom: {}'.format(state, symptom))
          
if(__name__=='__main__'):
    main()
