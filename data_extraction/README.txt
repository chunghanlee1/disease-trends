# Run the following on different machines to collect the data in parts:
bin/one_at_a_time.py --offset 0 --nterms 30 research/ncomms5212-s3.txt
bin/one_at_a_time.py --offset 30 --nterms 30 research/ncomms5212-s3.txt
bin/one_at_a_time.py --offset 60 --nterms 30 research/ncomms5212-s3.txt
# etc...
#Run the following to combine the files in "parts".
#Output is "combined.tsv" and a "summary.tsv" file.
bin/combine.py research/ncomms5212-s3.txt > summary.tsv
#Then run the following to extract the ones to redo
grep NoData summary.tsv > no_data.tsv
split no_data.tsv parts/nodata.
# Then redo them, optionally only getting US wide data
bin/redo.py --out parts/redo.aa.tsv --to_redo parts/nodata.aa
bin/redo.py --out parts/redo.aa.tsv --to_redo parts/nodata.aa --country_level

