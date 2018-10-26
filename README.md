DESCRIPTION <br />
Query symptoms data from the Google Trends API, then calculate correlation and conduct heirarchical clustering.<br />


INSTALLATION <br />
Software: <br />
	Python 3.6+ <br />
Required modules (installation instructions): <br />
	1. scipy 1.1.0 (https://www.scipy.org/install.html) <br />
	2. pytrends 4.4.0 (https://pypi.org/project/pytrends/) <br />
	3. numpy 1.14.3 (https://docs.scipy.org/doc/numpy-1.14.1/user/install.html)<br />
	4. pandas 0.23.0 (https://pandas.pydata.org/pandas-docs/stable/install.html)<br />


EXECUTION<br />
Set the 'CODE' folder as the working directory. Run the following files sequentially (warning: data collection may take up to thousands of hours due to rate limiting):<br />
	1. ?????<br />
	2. data_processing.py<br />
	3. cluster_corr.py<br />
Afterwards, the following files will be created:<br />
	1. combined.tsv<br />
	2. corr_by_state.csv<br />
	3. clusters_by_state.csv<br />
