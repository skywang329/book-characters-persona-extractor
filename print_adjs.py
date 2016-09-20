from graph_fns import *
from adjectives import *
from dict_methods import *
import pickle
import itertools
import pickle
import nltk
from nltk.corpus import wordnet as wn

with open('feelings.pkl', 'rb') as fp:
		feels = pickle.load(fp)

with open('variable.pkl', 'rb') as fp:
		variable = pickle.load(fp)
	
for key in  variable.keys():
	exec(key + " = variable['" + key + "']")

conjunctions = ["and", "or"]
stopwords = ["a", "and", "or", "but"]
forms_of_be = ["is", "was", "were", "be", "would", "will"]

def get_personas():
	parse_tree = init_parse_tree(sentence_token, norm_tok_list, norm_htok_list,
	 							pos_list, dep_list, ch_id_list, word_list,
	 							norm_word_list)

	adjs = init_adjs(parse_tree, sentence_token)

	(quote_set, quote_adjs) = append_quotes(parse_tree)
	subtract(adjs, quote_adjs)
	#chapter_indices = get_chapters(chapter_names, sentence_token, word_list)

	descs = get_describers(parse_tree, word_list, character, adjs, quote_adjs, 
						 itertools, stopwords, conjunctions, wn, feels, pov = False,
						 split_by_chapters = False, print_lines = False)
	
	return (parse_tree, adjs, quote_set, quote_adjs, descs)

(parse_tree, adjs, quote_set, quote_adjs, 
(describers, opinion_describers, all_describers)) = get_personas()

write_pickle(pickle, variable, parse_tree, describers, quote_set, adjs, 
				quote_adjs, opinion_describers, all_describers)