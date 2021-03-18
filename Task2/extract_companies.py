from ast import parse
import sys
import nltk

sys.path.append('..')

from Task2.utils import approximate_string_match, get_pr_metrics, partition_data, read_ce_data
import argparse
import json

company_map = {
    'realmex7pro' : 'realme',
    'iphone' : 'apple',
    'pocox3' : 'poco',
    'poco m2' : 'poco',
    'techno' : 'tecno',
    'one plus' : 'oneplus'
}

# corrected_company = {
#     'techno' : 'tecno',
#     'realmex7pro' : 'realme',
#     'iphone' : 'apple'
# }


def get_companies(ce_data):
    companies = set()
    for datum in ce_data:
        for company,sentiment in datum['companies']:
            companies.add(company)
    return companies

def map_companies(companies):
    for i in range(len(companies)):
        if companies[i] in company_map:
            companies[i] = company_map[companies[i]]
    return companies

def correct_company(company):
    if company in company_map:
        return company_map[company]
    else:
        return company

def predict_companies(datum, company_list, args):
    predicted_companies = set()
    tokens = nltk.word_tokenize(datum['raw_text'])

    print(datum['tweet_id'],'-------------------------------')
    print(datum['raw_text'])
    for token in tokens:
        for company in company_list:
            match_ratio = approximate_string_match(token.lower(),company.lower())
            if match_ratio >= args.token_match_threshold:
                print(token,company,match_ratio)
                predicted_companies.add(company)
    
    predicted_companies = set(map_companies(list(predicted_companies)))
    
    return list(predicted_companies)
    


def ce_fuzzymatch_eval(ce_data_dev, company_list, args):
    precision_numerator = 0
    precision_denominator = 0
    recall_numerator = 0
    recall_denominator = 0

    for datum in ce_data_dev:
        predictd_companies_list = predict_companies(datum,company_list, args)
        datum_metrics = get_pr_metrics(predictd_companies_list,[
            correct_company(x[0]) for x in datum['companies']
        ])
        precision_numerator += datum_metrics[0]
        precision_denominator += datum_metrics[1]
        recall_numerator += datum_metrics[2]
        recall_denominator += datum_metrics[3]
    
    return {
        'precision' : precision_numerator/precision_denominator,
        'recall' : recall_numerator/recall_denominator
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='')

    parser.add_argument('--labeled_csv_file_path',required=True)
    parser.add_argument('--dev_ratio',required=True,type=float)
    parser.add_argument('--token_match_threshold', type=float)
    
    args = parser.parse_args()

    ce_data = read_ce_data(args.labeled_csv_file_path)
    ce_data_train, ce_data_dev = partition_data(ce_data,args.dev_ratio)

    company_list = get_companies(ce_data_train)
    metrics = ce_fuzzymatch_eval(ce_data_dev,company_list,args)

    print(json.dumps(
        metrics,
        indent = 2
    ))

