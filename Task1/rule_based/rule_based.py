'''Rule based approach for task 1

This is a simple fuzzy string matching based implementation which checks if the word smartphone is present in the tweet.
It gives almost 99% accuracy on the train set 
'''
import pandas as pd 
import numpy as np 

from fuzzywuzzy import fuzz 
from sklearn.metrics import classification_report

def predict(x):
	'''Predictor function
	
	[description]
	
	Arguments:
		x {str} -- Input string
	
	Returns:
		float -- Probability of the tweet being relevant
	'''
	english_pred = fuzz.partial_ratio("smartphone",x.lower())
	hindi_pred = fuzz.partial_ratio("स्मार्टफ़ोन",x)
	return (max(hindi_pred,english_pred)>70)*1      # 70 here is a heuristic obtained on the train set!



if __name__ == '__main__':
	# Driver code to test
	data = pd.read_csv('dev_data_tweet.csv')
	y_pred = (data['Tweet'].apply(predict))
	y_true = data['Mobile_Tech_Tag']

	print(classification_report(y_true,y_pred))
	print("These are the mis-classified IDs")
	print(np.arange(4000)[y_true!=y_pred])
