#!/usr/bin/env python3
# vim: set tabstop=2 softtabstop=2 shiftwidth=2 noexpandtab colorcolumn=81 :
# VIM: let g:pyindent_open_paren=2 g:pyindent_continue=2
# -*- coding: utf-8 -*-
import matplotlib
matplotlib.use('Agg')
from matplotlib import rcParams, pyplot as plt
rcParams.update({'figure.autolayout': True})
from collections import Counter
import sys

nbins=100
#colors=('blue','red')
color='blue'
labels=('Visits','Terms')

def plot(counter, out, log, rotate):
	tuples = sorted(counter.items(), key=lambda x: x[1])
	counts = [t[1] for t in tuples]
	labels = [t[0] for t in tuples]

	plt.title("Cluster size Histogram")
	w=10
	h=4.6
	xlab='Symptom'
	ylab='Counts'
	if rotate:
		w, h = h, w
		xlab, ylab = ylab, xlab
	plt.figure(figsize=(w,h))
	plt.xlabel(xlab)
	plt.ylabel(ylab)
	plt.xticks(rotation=30)
	plt.tick_params(axis='both', which='major', labelsize=6)
	#plot.tick_params(axis='both', which='minor', labelsize=8)
	if rotate: fxn = plt.barh
	else: orientation = plt.bar
	fxn([i*1.2 for i in range(len(labels))], counts, height=1, tick_label=labels, color=color,log=log)
	plt.tight_layout()
	plt.savefig(out, dpi=300)

def parse_args():
	from argparse import ArgumentParser, FileType
	parser = ArgumentParser()
	parser.add_argument(
		'--log',
		action='store_true',
		default = False,
	)
	parser.add_argument(
		'--rotate',		
		action='store_true',
		default = False,
	)
	parser.add_argument(
		'clusters',
		type=FileType('r'),
		help='CSV File of symtom,pair,aggregate,month1,month2,etc',
	)
	parser.add_argument(
		'out',
		type=str,
		help='Image filename ending in .png,.svg, etc.'
	)
	parser.add_argument(
		'--corr_cutoff',
		type=float,
		default=0
	)

	args = parser.parse_args()
	return args

def parse_dict(c):
	members = c['members'].strip('"')
	return float(c['corr']),eval(members)

def parse_counts(counts, cutoff):
	from csv import DictReader
	counts = DictReader( counts )
	all_members = []
	for row in counts:
		corr, members = parse_dict(row)
		if corr > cutoff:
			all_members.extend( members )
	return Counter(all_members)

def main():
	args = parse_args()
	counts = parse_counts(args.clusters,args.corr_cutoff)
	plot(counts, args.out, args.log, args.rotate)

if __name__=='__main__':
	main()
