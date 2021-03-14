'''Rule based approach for task 1

This is a simple fuzzy string matching based implementation which checks if the word smartphone is present in the tweet.
It gives almost 99.9% accuracy on the train set 
'''
import pandas as pd 
import numpy as np 

from fuzzywuzzy import fuzz 
from sklearn.metrics import classification_report


def brute_force_fuzzy(s1,s2):
	# Returns the max match according to fuzzy matching
	return max(fuzz.ratio(s1,s2), fuzz.partial_ratio(s1,s2), fuzz.token_sort_ratio(s1,s2),fuzz.token_set_ratio(s1,s2))

def predict(x):
	'''Predictor function
	
	[description]
	
	Arguments:
		x {str} -- Input string
	
	Returns:
		float -- Probability of the tweet being relevant
	'''
	english_pred = brute_force_fuzzy("smartphone",x.lower())
	hindi_pred = brute_force_fuzzy("स्मार्टफ़ोन",x)
	return (max(hindi_pred,english_pred)>95)*1      # 95 here is a heuristic obtained on the train set!


def predict_exact(x):
	english_pred = int(any(["smartphone" in c.lower() for c in x]))
	hindi_pred = int(any(["स्मार्टफ़ोन" in c for c in x]))
	return max(hindi_pred,english_pred)      

if __name__ == '__main__':
	# Driver code to test
	data = pd.read_csv('dev_data_tweet.csv')
	y_pred = (data['Tweet'].apply(predict))
	y_true = data['Mobile_Tech_Tag']

	print(classification_report(y_true,y_pred))
	print("These are the mis-classified IDs")
	print(np.arange(4000)[y_true!=y_pred])
