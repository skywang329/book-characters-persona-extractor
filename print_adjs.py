from graph_fns import *
from adjectives import *
from dict_methods import *
import pickle
import itertools
import pickle
import json
import nltk
import pprint
import random

from nltk.corpus import wordnet as wn


with open('feelings.pkl', 'rb') as fp:
		feels = pickle.load(fp)

with open('variable.pkl', 'rb') as fp:
		variable = pickle.load(fp)
	
for key in  variable.keys():
	exec(key + " = variable['" + key + "']")

conjunctions = ["and", "or"]
stopwords = ["a", "and", "or", "but"]
bes = ["'s", "is", "was", "were", "be", "would", "'ll", "will"]
haves = ["'d", "had", "have", "has"]

def get_personas():
	parse_tree = init_parse_tree(sentence_token, norm_tok_list, norm_htok_list,
	 							pos_list, dep_list, ch_id_list, word_list,
	 							norm_word_list)

	adjs = init_adjs(parse_tree, sentence_token)

	(quote_set, quote_adjs) = append_quotes(parse_tree)
	subtract(adjs, quote_adjs)
	#chapter_indices = get_chapters(chapter_names, sentence_token, word_list)

	(descriptions, all_phrases) = get_describers(parse_tree, word_list, character, adjs, quote_adjs, 
						  					   itertools, stopwords, conjunctions, bes, haves, wn, feels, pov = False,
						  					   split_by_chapters = False, print_lines = False, differentiated = False)
	
	return (parse_tree, adjs, quote_set, quote_adjs, descriptions, all_phrases)

def write_json(sample_phrases):
	with open('descriptions_sample.json', 'w') as outfile:
		json.dump(sample_phrases, outfile)

(parse_tree, adjs, quote_set, quote_adjs, descriptions, all_phrases) = get_personas()

#describers = descriptions[0]
#opinion_describers = descriptions[1]
#all_describers = descriptions[2]

#print_personas(descriptions, character, differentiated = False)

print_phrases(all_phrases, pprint)

#print_sample_phrases(all_phrases, pprint, random)

sample_phrases = random.sample(all_phrases, len(all_phrases)/5)

#print_all_chars(all_describers, character)

#write_pickle(pickle, variable, parse_tree, descriptions, quote_set, adjs, 
#				quote_adjs)

write_json(sample_phrases)