#!/usr/bin/env bash
exe=choropleth/choropleth_data.py 
exe2=choropleth/intra_corr_filter.py

while read i
do
	{
		clust=clusters_by_state/$i.csv
		corr=corr_by_state/$i.csv	
		out=choropleth/$i.csv
		$exe $clust $corr $out
		clust=clusters_by_state/$i.corr_pvalue_filter.csv
		corr=corr_by_state/$i.corr_pvalue_filter.csv	
		out=choropleth/$i.corr_pvalue_filter.csv
		$exe $clust $corr $out 
		out=choropleth/$i.intracorr_cutoff.csv
		$exe2 .8 $clust $corr $out
	} &
done < corr_by_state/window_sizes.lst

wait
