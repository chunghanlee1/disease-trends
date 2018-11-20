#!/usr/bin/env bash

for f in data_processing/corr_by_state.*.csv
do
	data_analysis/cluster_corr.py $f &
done

wait
