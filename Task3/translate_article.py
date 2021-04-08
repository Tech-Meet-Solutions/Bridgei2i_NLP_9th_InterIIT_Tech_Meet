# -*- coding: utf-8 -*-
"""
Created on Mon Mar 15 17:56:11 2021

@author: Administrator
"""
import pandas as pd
import translators as ts
import sys
import unicodedata
def strip_control_chars(data: str) -> str:
    return ''.join(c for c in data if not unicodedata.category(c).startswith('C'))

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

def write(text):
	text = strip_control_chars(text)
	f = open("test.source", "a")
	f.write(text + ' ')
	f.close()
	return
		  
if __name__ == '__main__':
	low = int(sys.argv[1])
	hgh = int(sys.argv[2])
	df = pd.read_csv('evaluation_data.csv')
	
	sent = ""
	for j in range(low, hgh):
		for i in df['Text'][j]:
			if i in ["\n", "।"]:
				i = "."
			if i in [".", "?", "!"]:
				if sent != "":
					write(translate(sent + i))
				sent = ""
				continue
			sent += i
		write(translate(sent))
		sent = ""
		f = open("test.source", "a")
		f.write("\n")
		f.close()
		print("#############################",j, "Completed", "#####################")
