#!/usr/bin/env python3
# vim: set tabstop=2 softtabstop=2 shiftwidth=2 noexpandtab colorcolumn=81 :
# VIM: let g:pyindent_open_paren=2 g:pyindent_continue=2
from csv import DictReader

def parse_args():
	from argparse import ArgumentParser, FileType
	parser = ArgumentParser()
	parser.add_argument(
		'clusters',
		type=FileType('r'),
		nargs='+',
		help='CSV File of symtom,pair,aggregate,month1,month2,etc',
	)
	parser.add_argument(
		'out',
		type=str,
		help='Image filename ending in .png,.svg, etc.'
	)
	args = parser.parse_args()
	return args

def count(fh):
	reader = DictReader( fh )
	count = 0
	for row in reader:
		for k,v in row.items():
			if k in ('symptom','pair','aggregate','state'):
				continue
			try:
				f = float(v)
				count += 1
			except:
				pass
	return count

def main():
	args = parse_args()
	for f in args.clusters:
		c = count(f)
		print(f, c)

if __name__=='__main__':
	main()
