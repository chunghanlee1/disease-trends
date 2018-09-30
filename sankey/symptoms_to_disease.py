import pandas as pd

filepath = './disease-trends/data_extraction/research/'
df = pd.read_csv(filepath + 'ncomms5212-s2.txt', sep='\t')
