#!/usr/bin/env python3
# vim: set tabstop=2 softtabstop=2 shiftwidth=2 noexpandtab colorcolumn=81 :
# VIM: let g:pyindent_open_paren=2 g:pyindent_continue=2
# -*- coding: utf-8 -*-
from csv import DictReader,DictWriter
from os.path import splitext
from math import sqrt
#from scipy import stats

def parse_args():
	from argparse import ArgumentParser, FileType
	parser = ArgumentParser()
	parser.add_argument(
		'--corr_cutoff',
		type=float,
		default=None
	)
	parser.add_argument(
		'--pvalue_alpha',
		type=float,
		default=None
	)

	parser.add_argument(
		'in_file',
		type=FileType('r'),
		help='corr_by_state.*.csv'
	)
	parser.add_argument(
		'out_file',
		type=FileType('w'),
		help='corr_by_state.*.*_filter.csv'
	)

	args = parser.parse_args()
	return args

def pass_filter(corr, corr_cutoff, pvalue_alpha, window_size, t_table):
	if corr >= 1.0: return False
	if corr <= 0: return False
	if corr_cutoff is not None:
		if corr < corr_cutoff: return False
	if pvalue_alpha is not None:
		df = window_size -2
		t_alpha = t_table[df][pvalue_alpha]
		t = corr * sqrt(df) / sqrt(1-corr**2) 
		if t < t_alpha: return False
	return True

def parse_t_table():
	reader = DictReader(open('t_table.tsv'), delimiter='\t')
	t = {}
	for row in reader:
		new_row={}
		for k,v in row.items():
			if k != 'df': k = float(k)
			new_row[k] = float(v)
		t[ int(row['df']) ] = new_row
	return t

def main():
	args = parse_args()
	t_table = parse_t_table() if args.pvalue_alpha else None
	base = splitext(args.in_file.name)[0]
	window_size = int(base.rpartition('.')[2])
	window_size = window_size*2 + 1
	reader = DictReader( args.in_file )
	writer = DictWriter( args.out_file, fieldnames=reader.fieldnames )
	#bonferroni_out = splitext(args.out_file.name)[0]+'.bonferroni.csv'
	#bonferroni_fh = open(bonferroni_out, 'w')
	#bonferroni_writer = DictWriter( bonferroni_fh, fieldnames=reader.fieldnames )
	writer.writeheader()
	for row in reader:
		for field in reader.fieldnames:
			if field in ('symptom','pair','state'): continue
			if not row[field]: continue
			row[field] = float(row[field])
			if not pass_filter(row[field], args.corr_cutoff, args.pvalue_alpha, window_size, t_table):
				row[field] = ''
		writer.writerow(row)

if __name__=='__main__':
	main()
