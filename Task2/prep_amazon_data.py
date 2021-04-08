'''Pre-processes Amazon reviews data for our use case

Does the following - 
1. Convert jsonl to CSV after randomly sampling 10k examples
2. Keep 4k samples in English, translate 4k samples completely into Hindi, translate 2k samples partially into Hindi (see how to handle transliteration  -- TODO) 
'''

import argparse
import csv
import json 
import pandas
import random

import translators as ts

from tqdm import tqdm 

rating_to_sentiment = {1:-1,2:-1,3:0,4:1,5:1}


def clean_text_for_csv(text):
	'''
	Cleans text by removing commas, \n
	'''
	return text.replace("\n",' ').replace(",",".")

def sample_and_convert_to_csv(json_path,csv_path,num_samples=10000,json_length=1128437):
	'''
	Function to convert jsonl file to a sampled csv file having `num_samples` samples
	''' 
	samples = random.sample(range(json_length),num_samples)
	line_no = -1
	writer = csv.writer(open(csv_path,"w"))
	writer.writerow(["ID","Text","Sentiment","Rating"])	
	for line in tqdm(open(json_path).readlines()):
		line_no += 1
		if line_no not in samples:
			continue
		try:
			line_data = json.loads(line)
			row = [line_no,clean_text_for_csv(line_data["reviewText"]),rating_to_sentiment[int(line_data["overall"])],line_data["overall"]]
			writer.writerow(row)
		except Exception as e:
			print(line_no,e,line_data)


def translate(text):
	try:
		# print(text)
		t = ts.google(text,to_language='hi')
		t = t.replace("\n"," ")
		# print(t)
		return t
	except:
		print("--------------------OOPS (stop and try again)---------------------")
		return ""

# def 
if __name__ == '__main__':
	# sample_and_convert_to_csv("Cell_Phones_and_Accessories_5.json", "amazon_phones.csv")
	parser = argparse.ArgumentParser()
	""" Arguments: arg """
	parser.add_argument('--line_idx',type=int,default=0)
	parser.add_argument('--line_idx_max',type=int,default=4000)
	
	args = parser.parse_args()

	
	#  = 0
	# line_idx_max = 4000

	idx = 0
	writer = csv.writer(open("tweets_hindi.csv","a"),delimiter=",")
	reader = csv.reader(open("tweet_kaggle.csv"))
	for row in reader:
		if idx < args.line_idx:
			idx += 1
			continue
		if idx >= args.line_idx_max:
			break
		else:
			trans_text = translate(row[1])
			# print([row[0],trans_text,row[2],row[3]])
			writer.writerow([row[0],trans_text,row[2],row[3]])
			print("Wrote {} successfully".format(idx))
			idx += 1
