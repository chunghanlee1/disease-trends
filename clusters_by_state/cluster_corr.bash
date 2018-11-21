#!/usr/bin/env bash
while read i
do
	infile = corr_by_state/$i.csv
	outfile = clusters_by_state/$i.csv
	clusters_by_state/cluster_corr.py $infile $outfile &
	outfile=$i.corr_pvalue_filter.csv
	infile=corr_by_state/$outfile
	outfile=clusters_by_state/$outfile
	clusters_by_state/cluster_corr.py $infile $outfile # &
done < corr_by_state/window_sizes.lst

wait
