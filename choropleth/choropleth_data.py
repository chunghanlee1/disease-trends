#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
# VIM: let g:pyindent_open_paren=2 g:pyindent_continue=2
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import itertools as it
import sys

clust_path = sys.argv[1]
corr_path = sys.argv[2]
out = sys.argv[3]
# load the data
clusters = pd.read_csv(clust_path)
corrs = pd.read_csv(corr_path)

# list of rolling windows
years = np.arange(2005, 2018).astype(str)
months = [x.zfill(2) for x in np.arange(1, 13).astype(str)]
dates = ["-".join(x) for x in list(it.product(years, months))]
dates += ['2018-01','2018-02','2018-03','2018-04','2018-05','2018-06','2018-07','2018-08','2018-09']

# placeholder dataframe 
temp = pd.DataFrame(columns=['state','cluster','corr','members','window'])

# loop over each window
for window in dates:
	# select window data
    alpha = corrs[['symptom', 'pair', 'state', window]].rename(columns={window: 'window'})
    # only correlations of non-same pairs
    alpha = alpha[alpha.window<1] # remove all pair correlation = 1 [alpha.symptom!=alpha.pair]
    # select window data
    beta = clusters[clusters.period==window].drop(columns='period')
    
    # join on first symptom
    gamma = pd.merge(alpha, beta, on=['symptom', 'state'])
    # join on second symptom
    delta = pd.merge(gamma, beta, left_on=['pair', 'state'], right_on=['symptom', 'state']).drop(columns=['symptom_y']).rename(columns={'symptom_x': 'symptom', 'cluster_x':'symptom_cluster', 'cluster_y':'pair_cluster'})
    # filter symptom pairs that belong to the same cluster
    delta = delta[delta.symptom_cluster==delta.pair_cluster]
    # cosmetics
    delta = delta.drop(columns=['pair_cluster']).rename(columns={'symptom_cluster':'cluster'})
    
    # groupby clusters
    try:
        iota = delta.groupby(by=['state','cluster']).agg({'window': 'mean', 'symptom': lambda x: set(x), 'pair': lambda x: set(x)}).rename(columns={'window':'corr'})
        iota['members'] = iota.apply(lambda x: list(x['symptom'].union(x['pair'])), axis=1)
        iota = iota.drop(columns=['symptom', 'pair']).reset_index().groupby(by='state').apply(lambda x: x.loc[x['corr'] == x['corr'].max()]).drop(columns=['state']).reset_index().drop(columns=['level_1'])
        iota['window'] = window
    
        temp = temp.append(iota)
    except:
        pass

temp = temp.reset_index().drop('index', axis=1)
temp.to_csv(out, index=False)
