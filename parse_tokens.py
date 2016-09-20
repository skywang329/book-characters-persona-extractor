import pickle
from token_methods import *
pronouns = ({'I', 'me', 'my', 'mine', 'myself', 'you', 'your', 'yours',
			'yourself', 'he', 'him', 'his', 'himself', 'she', 'her',
			'hers', 'herself'})

file_ops()	 
varbles = init_vars(p_id = [], s_id = [], t_id = [], b_start = [], b_end = [],
		  wsp_after = [], h_id = [], word = [], norm_word = [], lemma = [],
		  pos = [], ner = [], dep = [], quote = [], ch_id = [], 
		  character_set_id = [], character = {})

(p_id, s_id, t_id, b_start, b_end, wsp_after, h_id, word, norm_word, lemma,
 pos, ner, dep, quote, ch_id, character_set_id, character) = varbles

varbles = (p_id, s_id, t_id, b_start, b_end, wsp_after, h_id, word,
 norm_word, lemma, pos, ner, dep, quote, ch_id, character_set_id,
 character)

varbles = fill_vars(p_id, s_id, t_id, b_start, b_end, wsp_after, h_id, word,
			norm_word, lemma, pos, ner, dep, quote, ch_id, 
			character_set_id, character)

(p_id, s_id, t_id, b_start, b_end, wsp_after, h_id, word, norm_word, lemma,
 pos, ner, dep, quote, ch_id, character_set_id, character) = varbles

map_characters(character)


print "Characters - "
print character

sentence_token = get_sentence_tokens(word, sentence_token = {})
lists = define_lists(sentence_token, t_id, h_id, word, norm_word, pos, ner, dep,
					 ch_id, quote, token_list = {}, htoken_list = {}, word_list = {},
					 norm_word_list = {}, pos_list = {}, ner_list = {}, dep_list = {}, ch_id_list = {},
					 quote_list = {}, norm_tok_list = {}, norm_htok_list = {}, all_quotes = set())
(token_list, htoken_list, word_list,
 norm_word_list, pos_list, ner_list, dep_list, ch_id_list,
 quote_list, norm_tok_list, norm_htok_list, all_quotes) = lists 

write_pickle(pickle, p_id, s_id, t_id, b_start, b_end, wsp_after, h_id,
			 word, norm_word, lemma, pos, ner, dep, quote, ch_id, 
			 character_set_id, character, sentence_token, token_list,
			 htoken_list, word_list, norm_word_list, pos_list, ner_list, 
			 dep_list, ch_id_list, quote_list, norm_tok_list, norm_htok_list,
			 all_quotes)