#!/usr/bin/env python3
# vim: set tabstop=2 softtabstop=2 shiftwidth=2 noexpandtab colorcolumn=81 :
# VIM: let g:pyindent_open_paren=2 g:pyindent_continue=2
from operator import itemgetter
from collections import Counter

def parse_args():
	from argparse import ArgumentParser, FileType
	parser = ArgumentParser(description='Find the most common clusters')
	parser.add_argument(
		'clusters',
		type=FileType('r'),
		help='CSV File of symtom,pair,aggregate,month1,month2,etc',
	)
	parser.add_argument(
		'--corr_cutoff',
		type=float,
		default=0
	)
	parser.add_argument(
		'--most_common',
		type=int,
		default=10
	)

	return parser.parse_args()

def parse_dict(c):
	members = c['members'].strip('"')
	return float(c['corr']),eval(members)

def parse_counts(fh, corr_cutoff):
	from csv import DictReader
	reader = DictReader( fh )
	all_clusters = []
	for row in reader:
		try: corr = float(row['corr'])
		except: continue
		if corr >= corr_cutoff:
			members = eval(row['members'])
			all_clusters.append( tuple( members ))
	return Counter(all_clusters)

def main():
	args = parse_args()
	counts = parse_counts(args.clusters, args.corr_cutoff)
	for k,v in counts.most_common(10):
		print(k,v)

if __name__=='__main__':
	main()
