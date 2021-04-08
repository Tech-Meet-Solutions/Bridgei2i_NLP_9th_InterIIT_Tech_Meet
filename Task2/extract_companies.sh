
python3 extract_companies.py \
    --labeled_csv_file_path ../data/evaluation_data.tsv \
    --dev_ratio 1.0 \
    --token_match_threshold 0.81 \
    --read_companies  \
    --company_json_path ../data/company_all.json \
    --data_type  articles \
    --sentence_context_window 2 \
    --skip_first_line \
    --data_json_out_path ../data/evaluation_data.json \
    --eval off








# python3 extract_companies.py \
#     --labeled_csv_file_path ../data/tweet_concatenated.tsv \
#     --dev_ratio 1.0 \
#     --token_match_threshold 0.81 \
#     --read_companies  \
#     --company_json_path ../data/company_all.json \
#     --data_type  tweets \
#     --sentence_context_window 2 \
#     --skip_first_line \
#     --data_json_out_path ../data/dev_data_tweet.json








# python3 extract_companies.py \
#     --labeled_csv_file_path ../data/dev_data_article_3701_3850.tsv \
#     --dev_ratio 1.0 \
#     --token_match_threshold 0.81 \
#     --read_companies  \
#     --company_json_path ../data/company_all.json \
#     --data_type  articles \
#     --sentence_context_window 2 \
#     --skip_first_line \
#     --data_json_out_path ../data/dev_data_article.json









# python3 extract_companies.py \
#     --labeled_csv_file_path ../data/dev_data_article_3701_3850.tsv \
#     --dev_ratio 1.0 \
#     --token_match_threshold 0.81 \
#     --read_companies  \
#     --company_json_path ../data/company.json \
#     --data_type  articles \
#     --sentence_context_window 2 \
#     --skip_first_line \
#     --data_json_out_path ../data/dev_data_article.json