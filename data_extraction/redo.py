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
    parser.add_argument(
     '--country_level',
     required=False,
     default=False,
     action='store_true'
    )
    args = parser.parse_args()
    return args

def fetch_data(symptom, state, country_level):
    geo = 'US' 
    if country_level is None:
        geo += '-'+state
    elif state in country_level:
            return country_level[state]
    for i in range(1):
        try:
            pytrend.build_payload(kw_list=[symptom], timeframe= 'all', geo=geo)
            interest_over_time_df = pytrend.interest_over_time()
            #if 'date' not in interest_over_time_df:
            #    time.sleep(randint(20,30))
            #    continue
            interest_over_time_df['state']=state
            interest_over_time_df['symptom']=symptom
            if country_level is not None:
                country_level[state] = interest_over_time_df
            print('Downloaded data for State: {}, Symptom: {}'.format(state, symptom))
            return interest_over_time_df
            time.sleep(randint(40,55))
            break
        except:
            print('Try again for {},{}'.format(state, symptom))
            time.sleep(randint(40,55))
            continue

def main():
    args = parse_args()
    country_level = {} if args.country_level else None
    # Login to Google. Only need to run this once, the rest of requests will use the same session.
    pytrend = TrendReq()
    reader = DictReader(args.to_redo, fieldnames=['symptom', 'state', 'status'], delimiter='\t')
    for row in reader:
        symptom = row['symptom']
        #symptom = re.sub('[^0-9a-zA-Z]+', ' ', symptom)
        state = row['state']
        print(symptom,state)
        #For each state, fetch data...
        interest_over_time_df = fetch_data(symptom, state, country_level)
        interest_over_time_df.to_csv(args.out, sep=',', encoding='utf-8')
           
if(__name__=='__main__'):
    main()
