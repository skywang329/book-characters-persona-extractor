import pickle
import json
import nltk
from nltk.corpus import wordnet as wn
#from wordnet_methods import *

feeling = wn.synset('feeling.n.01')
happy = wn.synset('happiness.n.01')

def get_hyponyms(li):
	return [x.hyponyms() for x in li]

def flatten(li):
	return [item for sublist in li for item in sublist]

def get_hyponyms_list(li):
	if li:
		return list(set(flatten(get_hyponyms(li))))

def get_the_hyponyms(li, hyps):
	if li:
		hyps |= set(li)
		get_the_hyponyms(get_hyponyms_list(li), hyps)
	return hyps

def get_all_hyponyms(li):
	hyps = set()
	return get_the_hyponyms(li, hyps)

def write_pickle(feels):
	with open('feelings.pkl', 'wb') as fp:
		pickle.dump(feels, fp, pickle.HIGHEST_PROTOCOL)

feels = set(sorted(get_all_hyponyms([feeling])))


feeleys = set()
for x in feels:
	feeleys.add(str(x))
feels = feeleys

print feels

write_pickle(feels)
#def write_json():
#	data = {'feels': feels}

#	with open('feelings.json', 'w') as fp:
 #   		json.dump(data, fp, sort_keys=True, indent=4)

#write_json()

