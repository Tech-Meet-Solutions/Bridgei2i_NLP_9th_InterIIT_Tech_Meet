output_file_path=/content/drive/MyDrive/projects/data/interIIT_NLP_task/out/3251_3500.txt

mkdir -p $(dirname $output_file_path)

low=3251
high=3500

while [ $low -le $high ]
do
	python3 translate_article.py \
		--low $low \
		--high $(($low+9)) \
		--article_file_path /content/drive/MyDrive/projects/data/interIIT_NLP_task/dev_data_article.csv \
		--output_file_path $output_file_path
	low=$((low+10))
done
