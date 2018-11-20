#!/usr/bin/env bash

#for i in 1 6 12 24 48
for i in 1 12 24 48
do
	data_processing/choropleth_data.py $i &
done

wait
