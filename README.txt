DESCRIPTION 
The Python code (???) queries symptoms data from the Google Trends API, then 'data_processing.py' is used to calculate rolling window correlation between symptom pairs from raw trend data. Calculated correlation is separated by state and time period (i.e. rolling window). Finally, 'cluster_corr.py' runs heirarchical clustering on the correlation data, using correlation as the distance metric (higher positive correlation -> similar).

INSTALLATION
Software:
	Python 3.6+
Required modules (installation instructions):
	1. scipy 1.1.0 (https://www.scipy.org/install.html)
	2. pytrends 4.4.0 (https://pypi.org/project/pytrends/)
	3. numpy 1.14.3 (https://docs.scipy.org/doc/numpy-1.14.1/user/install.html)
	4. pandas 0.23.0 (https://pandas.pydata.org/pandas-docs/stable/install.html)

EXECUTION
Run the following steps sequentially from the command line or using IDE
(warning: data collection will take thousands of hours due to rate
limiting. We performed this step using many IP addresses):
	1. cd data_extraction and follow the instructions in README.txt
	2. data_processing/data_processing.bash
	3. data_analysis/cluster_corr.bash
	4. data_processing/choropleth_data.bash
Afterwards, the following files will be created:
	1. data_extraction/combined.tsv
	2. data_processing/corr_by_state.<window size>.csv
	3. data_analysis/clusters_by_state.<window size>.csv
	4. data_processing/choropleth_data.<window size>.csv
FIGURES:
	1. cd data_processing
	2. ./cluster_member_histo.py choropleth_data.1.csv cluster_histo.1.png --rotate --corr_cutoff .96
	2. ./cluster_member_histo.py choropleth_data.48.csv cluster_histo.48.png --rotate --corr_cutoff .60
	3 ./cluster_size_histo.py choropleth_data.1.csv cluster_size_histo.1.png --rotate --corr_cutoff .5 
	3 ./cluster_size_histo.py choropleth_data.48.csv cluster_size_histo.48.png --rotate --corr_cutoff .5 
