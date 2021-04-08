#!/bin/bash

i=0
while [ $i -le 3780 ]
do
	j=$(($i+20))
	python3 prep_amazon_data.py --line_idx $i --line_idx_max $j
	# python3 translate_article.py $i $j
	#echo $i
	#echo $j
	i=$j
done
