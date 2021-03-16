low=3251
high=3500
output_file_path=/Users/amankansal/Desktop/data/interIIT_NLP_task/out/$low-$high.source

mkdir -p $(dirname $output_file_path)

python3 translate_article.py \
	--low 3251 \
	--high 3350 \
	--article_file_path /Users/amankansal/Desktop/data/interIIT_NLP_task/dev_data_article.csv \
	--output_file_path $output_file_path