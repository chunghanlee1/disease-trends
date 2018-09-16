#!/usr/bin/env python3.6
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
# VIM: let g:pyindent_open_paren=2 g:pyindent_continue=2
# -*- coding: utf-8 -*-
"""
@author: Gordon Lemmon
"""

import time
from glob import glob
from csv import DictReader
from copy import deepcopy

#Initiate data & variables
states = [
        "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", 
        "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
        "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
        "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
        "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"
]

def parse_args():
    from argparse import ArgumentParser, FileType
    parser = ArgumentParser(description='Calculate p-values for pairs of terms')
    parser.add_argument(
        '--out_prefix',
        default='combined',
        help='Tab delimited file. First column is the symptom descriptor',
    )
    parser.add_argument(
        'symptoms',
        type=FileType('r'),
        help='Tab delimited file. First column is the symptom descriptor',
    )
    args = parser.parse_args()
    return args

def parse_symptoms(path, symptoms_dict):
    symptoms = deepcopy(symptoms_dict)
    with open(path) as fh:
        reader = DictReader(filter(lambda x:not x.startswith(','), fh))
        row = next(reader)
        print(row)
        sym = row['symptom']
        rel_freq = row[sym]
        del row[sym]
        row['trend'] = rel_freq
        symptoms[sym][row['state']][row['date']]=row
    return symptoms

def main():
    args = parse_args()
    # Login to Google. Only need to run this once, the rest of requests will use the same session.
    symptom_list = [r.strip().split('\t')[0] for r in args.symptoms][1:]
    symptoms_dict={s:{st:{} for st in states} for s in symptom_list}
    symptoms=[]
    for path in glob('parts/*'):
        symptoms.append(parse_symptoms(path, symptoms_dict))
          
    for symptom in symptom_list:
        for state in states:
            symptom_results = [s[symptom][state] for s in symptoms]
            symptom_results.sort(key=lambda x: len(x), reverse=True)
            result = symptom_results[0]
            print(symptom, state, len(result[0]))

if(__name__=='__main__'):
    main()
