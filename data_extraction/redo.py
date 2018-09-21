#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
# VIM: let g:pyindent_open_paren=2 g:pyindent_continue=2
# -*- coding: utf-8 -*-
"""
@author: Gordon Lemmon
"""

from pytrends.request import TrendReq
from pytrends.exceptions import ResponseError
import time
from csv import DictReader, DictWriter
from random import randint
import re

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
        '--out',
        required=True,
        type=FileType('w'),
        help='Tab delimited file. First column is the symptom descriptor',
    )
    parser.add_argument(
        '--to_redo',
        required=True,
        type=FileType('r'),
        help='Tab delimited file of symptom, state',
    )

    args = parser.parse_args()
    return args

def main():
    args = parse_args()
    # Login to Google. Only need to run this once, the rest of requests will use the same session.
    pytrend = TrendReq()
    reader = DictReader(args.to_redo, fieldnames=['symptom', 'state', 'status'], delimiter='\t')
    for row in reader:
        symptom = row['symptom']
        symptom = re.sub('[^0-9a-zA-Z]+', ' ', symptom)
        state = row['state']
        print(symptom,state)
        #For each state, fetch data...
        # Need to extract data relative to a baseline. Here we use "cough"
        for i in range(5):
            try:
                pytrend.build_payload(kw_list=[symptom], timeframe= 'all', geo='US-'+state)
                interest_over_time_df = pytrend.interest_over_time()
                #if 'date' not in interest_over_time_df:
                #    time.sleep(randint(20,30))
                #    continue
                interest_over_time_df['state']=state
                interest_over_time_df['symptom']=symptom
                interest_over_time_df.to_csv(args.out, sep=',', encoding='utf-8')
                print('Downloaded data for State: {}, Symptom: {}'.format(state, symptom))
                time.sleep(randint(40,55))
                break
            except:
                print('Try again for {},{}'.format(state, symptom))
                time.sleep(randint(40,55))
                continue
          
if(__name__=='__main__'):
    main()
