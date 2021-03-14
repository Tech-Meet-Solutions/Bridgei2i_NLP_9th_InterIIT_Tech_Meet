import re 
import numpy as np
import random

from copy import deepcopy
from fuzzywuzzy import fuzz

np.random.seed(42)
random.seed(42)

def preprocess_clean(s):
    s=  re.sub('^(\+\d{1,2}\s)?\(?\d{4}\)?[\s.-]\d{3}[\s.-]\d{3}$','', s)
    s=  re.sub('^(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}$','', s)
    s=  re.sub('\d{10}$','', s)#phone numbers
    s=  re.sub('^(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}$','', s)#phone numbers
    s=  re.sub('\d{10,9,8,7,6,11,12}$','', s)
    s = re.sub('http\S+', '', s)  # remove URLs
    s = re.sub('www\S+', '', s)
    s = re.sub('RT|cc', '', s)  # remove RT and cc
    s = re.sub('#\S+', '', s)  # remove hashtags
    s = re.sub('@\S+', '', s)  # remove mentions
    s = re.sub('[%s]' % re.escape("""!"#$%&'()*+-/:;<=>@[\]^_`{|}~"""), ' ', s)  


    cleanr = re.compile('<.*?>')
    s = re.sub(r'\d+', '', s)
    s = re.sub(cleanr, '', s)
    s = re.sub("'", '', s)
    s = re.sub(r'\W+', ' ', s)
    s = s.replace('_', '')

    return s

def parse_ce_data_line(line):
    line = line.strip()
    line = line.split('\t')
    tweet_id, raw_text, companies = line[:3]

    if len(line)>3:
        sentiment = int(line[4])
    
    if ',' in companies:
        companies = companies.strip().split(',')
    else:
        companies = [companies]

    return {
        'tweet_id' : tweet_id,
        'raw_text' : raw_text,
        'text' : preprocess_clean(raw_text),
        'companies':[
            (company,sentiment) for company in companies
        ]
    }

def read_ce_data(ce_data_path):
    ce_data = []
    with open(ce_data_path) as ce_data_file:
        for line in ce_data_file:
            datum = parse_ce_data_line(line)
            if datum['tweet_id'] == ce_data[-1]['tweet_id']:
                ce_data[-1]['companies'].extend(
                    datum['companies']
                )
            else:
                ce_data.append(datum)
    return ce_data

def partition_data(data,dev_ratio):
    data = deepcopy(data)
    dev_size = int(len(data)*dev_ratio)
    random.shuffle(data)
    return data[:-dev_size], data[-dev_size:]

def get_pr_metrics(predicted_set, gold_set):
    precision_numerator = sum(
        [
            1 if x in gold_set else 0 for x in predicted_set
        ]
    )

    precision_denominator = len(predicted_set)

    recall_numerator = sum(
        [
            1 if x in predicted_set else 0 for x in gold_set
        ]
    )

    recall_denominator = len(gold_set)

    return (
        precision_numerator,
        precision_denominator,
        recall_numerator,
        recall_denominator
    )

def approximate_string_match(str1, str2):
    return max(
        fuzz.ratio(str1,str2),
        fuzz.partial_ratio(str1, str2),
        fuzz.token_sort_ratio(str1, str2),
        fuzz.token_set_ratio(str1,str2),
        fuzz.partial_token_set_ratio(str1, str2),
        fuzz.partial_token_sort_ratio(str1, str2)
    )

