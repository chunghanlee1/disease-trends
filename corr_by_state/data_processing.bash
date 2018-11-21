#!/usr/bin/env bash

while read i; do
	{
		./data_processing.py $i 
		out=$i.corr_filter.csv
		./filter_corr_by_state.py --corr_cutoff 0.5 $base.csv $out 
		out=$i.pvalue_filter.csv
		./filter_corr_by_state.py --pvalue_alpha 0.05 $base.csv $out 
		out=$i.corr_pvalue_filter.csv
		./filter_corr_by_state.py --corr_cutoff 0.5 --pvalue_alpha 0.05 $i.csv $out 
	} &
done < window_sizes.lst
wait
