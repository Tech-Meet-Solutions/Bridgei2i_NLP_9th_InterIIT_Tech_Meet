'''Rule based approach for task 1

This is a simple fuzzy string matching based implementation which checks if the word smartphone is present in the tweet.
It gives almost 99.9% accuracy on the train set 
'''
import pandas as pd 
import numpy as np 

from fuzzywuzzy import fuzz 
from sklearn.metrics import classification_report

# target_words = ['smartphone','स्मार्टफ़ोन','camera','android','स्मार्टफोन','earphones','फ़ोन','कैमरा','phone', 'samsung','xiaomi']
target_words = ['smartphone','camera','earphones', 'samsung','xiaomi','iphone','blackberry','nokia','oneplus','mediatek','motorola']
hindi_words = ['स्मार्टफ़ोन', 'स्मार्टफोन',  'कैमरा',]
def brute_force_fuzzy(s1,s2):
	# Returns the max match according to fuzzy matching
	return max(fuzz.ratio(s1,s2), fuzz.partial_ratio(s1,s2), fuzz.token_sort_ratio(s1,s2),fuzz.token_set_ratio(s1,s2))


def search_exact(word,string):
	return int(any([word in c for c in string.split()]))
def predict(x):
	'''Predictor function
	
	[description]
	
	Arguments:
		x {str} -- Input string
	
	Returns:
		float -- Probability of the tweet being relevant
	'''
	pred = max([brute_force_fuzzy(word,x.lower()) for word in target_words])
	pred_hind = max([search_exact(word,x) for word in hindi_words])
	# english_pred = max(brute_force_fuzzy("smartphone",x.lower()),brute_force_fuzzy("device",x.lower()))
	# hindi_pred = max(brute_force_fuzzy("स्मार्टफ़ोन",x),brute_force_fuzzy("स्मार्टफोन",x))
	return max((pred>95)*1,pred_hind)      # 95 here is a heuristic obtained on the train set!


def predict_exact(x):
	english_pred = int(any(["smartphone" in c.lower() for c in x]))
	hindi_pred = int(any(["स्मार्टफ़ोन" in c for c in x]))
	return max(hindi_pred,english_pred)      

if __name__ == '__main__':
	# Driver code to test
	data = pd.read_csv('evaluation_data.csv')
	print("lol")
	print(data)
	data['Flag'] = (data['Text'].apply(predict))
	# y_true = data['Mobile_Tech_Flag']
	# print(np.isinf(y_pred.any()),np.isinf(y_true.any()))
	# col_mask=y_true.isnull()
	# print(col_mask[col_mask==True].index)
	# print((y_pred==y_true).sum())
	# print(y_pred-y_true)
	# print(classification_report(y_true,y_pred))
	# print("These are the mis-classified IDs")
	# idx = np.arange(4000)[y_true!=y_pred]
	# print(idx)

	data.to_csv('eval_preds_hindi.csv')
