DESCRIPTION
Query symptoms data from the Google Trends API, then calculate correlation and conduct heirarchical clustering.


INSTALLATION 
Software: 
	Python 3.6+
Required modules (installation instructions):
	1. scipy 1.1.0 (https://www.scipy.org/install.html)
	2. pytrends 4.4.0 (https://pypi.org/project/pytrends/)
	3. numpy 1.14.3 (https://docs.scipy.org/doc/numpy-1.14.1/user/install.html)
	4. pandas 0.23.0 (https://pandas.pydata.org/pandas-docs/stable/install.html)


EXECUTION 
Set the 'CODE' folder as the working directory. Run the following files sequentially (warning: data collection may take up to thousands of hours due to rate limiting):
	1. ?????
	2. data_processing.py
	3. cluster_corr.py
Afterwards, the following files will be created:
	1. combined.tsv
	2. corr_by_state.csv
	3. clusters_by_state.csv
