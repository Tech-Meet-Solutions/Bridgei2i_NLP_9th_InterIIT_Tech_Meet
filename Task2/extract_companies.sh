python3 extract_companies.py \
    --labeled_csv_file_path /Users/amankansal/Desktop/data/interIIT_NLP_task/dev_data_article_3701_3850.tsv \
    --dev_ratio 1.0 \
    --token_match_threshold 0.81 \
    --read_companies  \
    --company_json_path /Users/amankansal/Desktop/data/interIIT_NLP_task/company.json \
    --data_type  articles \
    --sentence_context_window 2 \
    --skip_first_line \
    --data_json_out_path /Users/amankansal/Desktop/data/interIIT_NLP_task/dev_data_article.json