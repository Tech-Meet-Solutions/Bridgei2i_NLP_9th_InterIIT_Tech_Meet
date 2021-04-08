#!/bin/bash

i=0
while [ $i -le 224 ]
do
    j=$(($i+1))
    python3 translate_article.py $i $j
    #echo $i
    #echo $j
    i=$j
done
