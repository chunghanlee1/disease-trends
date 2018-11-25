#!/usr/bin/env python3
# vim: set tabstop=2 softtabstop=2 shiftwidth=2 noexpandtab colorcolumn=81 :
# VIM: let g:pyindent_open_paren=2 g:pyindent_continue=2
# -*- coding: utf-8 -*-

from argparse import ArgumentParser, FileType
from itertools import combinations
from csv import DictReader

def parse_args():
	parser = ArgumentParser(description='Find the percent of clusters that contain the terms listed in the cmdline arguments, optionally restricting between two dates')
	parser.add_argument(
		'clusters',
		type=FileType('r'),
		help='CSV File of state,cluster,corr,members',
	)
	parser.add_argument(
		'--dates',
		nargs=2,
		default=None,
		help='formatted as yyyy-mm'
	)
	parser.add_argument(
		'--terms',
		nargs='+',
		default=0
	)

	return parser.parse_args()

def parse_date(date):
	if '-' in date:
		date = date.split('-')
		return int(date[0]), int(date[1])
	return int(date)

def parse_dates(dates):
	dates = [parse_date(d) for d in dates]
	if type(dates[0]) == int and dates[0] > dates[1]:
		dates[1] += 12
	return dates

def date_filter(dates, date):
	if not dates: return True
	yr,mo = parse_date(date)
	if type(dates[0]) == int:
		if mo < dates[0]:
			mo += 12
		if mo > dates[1]: return False
	else:
		if yr < dates[0][0]: return False
		if yr > dates[1][0]: return False
		if yr == dates[0][0] and mo < dates[0][1]: return False
		if yr == dates[1][0] and mo > dates[1][1]: return False
	return True

def count(clusters, terms, dates):
	if dates:
		dates = parse_dates(dates)
	clusters = DictReader( clusters )
	n = 0
	pair_terms = {pair:0 for pair in combinations(terms,2)}
	terms = {tuple([term]):0 for term in terms}
	terms.update(pair_terms)
	for row in clusters:
		if not date_filter(dates, row['window']):
			continue
		n += 1
		members = eval(row['members'])
		for k,v in terms.items():
			if all([t in members for t in k]):
				terms[k] += 1
	for k,v in terms.items():
		print(*k, round(v/n*100, 2))


def main():
	args = parse_args()
	count(args.clusters,args.terms, args.dates)

if __name__=='__main__':
	main()
