import re 
import numpy as np
import random
import pdb, traceback
import sys

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

def parse_ce_data_line(line,args):
    try:
        line = line.strip()
        line = line.split('\t')
        doc_id, raw_text = line[:2]

        raw_text = raw_text.replace('।','.')

        basic_datum_size = 3 if args.data_type == 'tweets' else 5

        if len(line)>basic_datum_size:
            if args.data_type == 'tweets':
                companies = line[2]
                sentiments = line[3]
                if ',' in companies:
                    companies = companies.strip().split(',')
                else:
                    companies = [companies]
                
                if ',' in sentiments:
                    sentiments = list(map(int,sentiments.strip().split(',')))
                else:
                    sentiments = [int(sentiments)]
                
            else:
                companies = line[4::2]
                sentiments = line[5::2]
                sentiments = [int(x) for x in sentiments]

            companies = [x.strip().lower() for x in companies]


        else:
            companies = []
            sentiments = []
        
        # if '' in companies:
        #     raise NotImplementedError

        return {
            'doc_id' : doc_id,
            'raw_text' : raw_text,
            'text' : preprocess_clean(raw_text),
            'companies':[
                (company,sentiment) for company,sentiment in zip(companies,sentiments) if company!=''
            ]
        }
    except:
        traceback.print_exc(file=sys.stdout)
        pdb.set_trace()

def read_ce_data(ce_data_path, args):
    try:
        ce_data = []
        with open(ce_data_path) as ce_data_file:
            ce_data_lines = ce_data_file.readlines()
            if args.skip_first_line:
                ce_data_lines=ce_data_lines[1:]
            for line in ce_data_lines:
                if line.strip() == '':
                    continue
                datum = parse_ce_data_line(line,args)
                if not len(ce_data) == 0 and datum['doc_id'] == ce_data[-1]['doc_id']:
                    ce_data[-1]['companies'].extend(
                        datum['companies']
                    )
                else:
                    ce_data.append(datum)
        return ce_data
    except:
        traceback.print_exc(file=sys.stdout)
        pdb.set_trace()

def partition_data(data,dev_ratio):
    data = deepcopy(data)
    dev_size = int(len(data)*dev_ratio)
    random.shuffle(data)
    return data[:len(data)-dev_size], data[len(data)-dev_size:]

def get_pr_metrics(predicted_set, gold_set):
    
    precision_numerator = sum(
        [
            1 for x in predicted_set if x in gold_set
        ]
    )

    precision_denominator = len(predicted_set)

    recall_numerator = sum(
        [
            1 for x in gold_set if x in predicted_set
        ]
    )

    recall_denominator = len(gold_set)

    if recall_numerator!=recall_denominator:
        print('predicted',predicted_set)
        print('gold',gold_set)
        print()

    return (
        precision_numerator,
        precision_denominator,
        recall_numerator,
        recall_denominator
    )

def approximate_string_match(str1, str2):
    if len(str2)>=4 and str2 in str1:
        return 1
    if str2 == 'iphone' and str2 not in str1:
        return 0
    return max(
        fuzz.ratio(str1,str2),
        # fuzz.partial_ratio(str1, str2),
        # fuzz.token_sort_ratio(str1, str2),
        # fuzz.token_set_ratio(str1,str2),
        # fuzz.partial_token_set_ratio(str1, str2),
        # fuzz.partial_token_sort_ratio(str1, str2),
        0
    ) /100

def get_context_sentences(sentences,i,context_window):
    return sentences[
        max(0,i-context_window):i+context_window+1
    ]

