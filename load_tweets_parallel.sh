#!/bin/sh

files=$(find data/*)


echo '================================================================================'
echo 'load pg_normalized'
echo '================================================================================'
## FIXME: implement this with GNU parallel
time echo "$files" | parallel ./load_normalized.sh


#echo '================================================================================'
#echo 'load pg_normalized_batch'
#echo '================================================================================'
# FIXME: implement this with GNU parallel
#time echo "$files" | parallel ./load_normalized_batch.sh




