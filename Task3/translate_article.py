# -*- coding: utf-8 -*-
"""
Created on Mon Mar 15 17:56:11 2021

@author: Administrator
"""
import pandas as pd
import translators as ts
import argparse
from tqdm import tqdm

import multiprocessing

def translate(text):
	try:
		print(text)
		t = ts.google(text,to_language='en')
		t = t.replace("\n"," ")
		print(t)
		return t
	except:
		print("--------------------OOPS (stop and try again)---------------------")
		return ""

# def write(text, output_file_path):
# 	f = open(output_file_path, "a")
# 	f.write(text + ' ')
# 	f.close()
# 	return

def translate_para(para):
	translated_para = ""
	sent = ""
	for i in para:
		if i in ["\n", "।"]:
			i = "."
		if i in [".", "?", "!"]:
			if sent != "":
				translated_sentence = translate(sent + i)
				translated_para += translated_sentence + ' '
			sent = ""
			continue
		sent += i
	return translated_para
		  
if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='')

	parser.add_argument('--low',required=True,type=int)
	parser.add_argument('--high',required=True,type=int)
	parser.add_argument('--article_file_path',required=True)
	parser.add_argument('--output_file_path',required=True)

	args = parser.parse_args()

	low = args.low
	hgh = args.high
	df = pd.read_csv(args.article_file_path)
	
	sent = ""
	paras = df['Text'][low:hgh+1]

	pool = multiprocessing.Pool(8)
	translated_paras = pool.map(translate_para,tqdm(paras))
	pool.close()

	with open(args.output_file_path,'a') as output_file:
		output_file.writelines(translated_paras)
	


	# for j in tqdm(range(low, hgh)):
	# 	for i in df['Text'][j]:
	# 		if i in ["\n", "।"]:
	# 			i = "."
	# 		if i in [".", "?", "!"]:
	# 			if sent != "":
	# 				write(translate(sent + i),args.output_file_path)
	# 			sent = ""
	# 			continue
	# 		sent += i
		# write('\n')
		# print("#############################",j, "Completed", "#####################")