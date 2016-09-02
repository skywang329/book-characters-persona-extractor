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
def form_of_be(parse_tree, a, i):
	return ([tup for tup in parse_tree[i] if 
			is_norm_word_equal(tup, "was") or 
			is_norm_word_equal(tup, "were") or 
			is_norm_word_equal(tup, "is") or
			is_norm_word_of(tup, "be") or 
			is_norm_word_of(tup, "would") or
			is_norm_word_of(tup, "will") and
			is_parent(tup, a, i)])

chapter_names = (['PROLOGUE .','BRAN .','CATELYN .','DAENERYS .','EDDARD .',
				'JON .','CATELYN .','ARYA .','BRAN .','TYRION .','JON .',
				'DAENERYS .','EDDARD .','TYRION .','CATELYN .','SANSA .',
				'EDDARD .','BRAN .','CATELYN .','JON .','EDDARD .','TYRION .',
				'ARYA .','DAENERYS .','BRAN .','EDDARD .','JON .','EDDARD .',
				'CATELYN .','SANSA .','EDDARD .','TYRION .','ARYA .',
				'EDDARD .','CATELYN .','EDDARD .','DAENERYS .','BRAN .',
				'TYRION .','EDDARD .','CATELYN .','JON .','TYRION .',
				'EDDARD .','SANSA .','EDDARD .','DAENERYS .','EDDARD .',
				'JON .','EDDARD .','ARYA .','SANSA .','JON .','BRAN .',
				'DAENERYS .','CATELYN .','TYRION .','SANSA .','EDDARD .',
				'CATELYN .','JON .','DAENERYS .','TYRION .','CATELYN .',
				'DAENERYS .','ARYA .','BRAN .','SANSA .','DAENERYS .',
				'TYRION .','JON .','CATELYN .','DAENERYS .'])

parse_tree = init_parse_tree(sentence_token, norm_tok_list, norm_htok_list,
 							pos_list, dep_list, ch_id_list, word_list,
 							norm_word_list)

adjs = init_adjs(parse_tree, sentence_token)

(quote_set, quote_adjs) = append_quotes(parse_tree)
subtract(adjs, quote_adjs)

chapter_indices = get_chapters(chapter_names, sentence_token, word_list)

out = get_describers(parse_tree, word_list, character, adjs, quote_adjs, 
					 itertools, stopwords, conjunctions, wn, feels, pov = False,
					 split_by_chapters = False, print_lines = True)
(describers, opinion_describers, all_describers) = out

write_pickle(pickle, variable, parse_tree, describers, quote_set, adjs, 
				quote_adjs, opinion_describers, all_describers)