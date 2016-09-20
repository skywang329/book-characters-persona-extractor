def file_ops():
	#file0 = open('/home/nikhil/Documents/Project/hp_tokens.txt', 'r')
	#file  = open('/home/nikhil/Documents/Project/hp_parsed.txt', 'w')
	file0 = open('C:/Users/Nikhil Prabhu/Documents/Programming/Project/hp_tokens.txt', 'r')
	file = open('C:/Users/Nikhil Prabhu/Documents/Programming/Project/hp_parsed.txt', 'w')

	for line in file0:
		file.write(line.replace('\t', ' '))
		#file.write(line.replace('. . .', '...'))
	file0.close()
	file.close()

	#file = open('/home/nikhil/Documents/Project/hp_parsed.txt', 'r')	

def init_vars(p_id, s_id, t_id, b_start, b_end, wsp_after, h_id, word,
				norm_word, lemma, pos, ner, dep, quote, ch_id, 
				character_set_id, character):
	
	#file = open('/home/nikhil/Documents/Project/hp_parsed.txt', 'r')	
	file = open('C:/Users/Nikhil Prabhu/Documents/Programming/Project/hp_parsed.txt', 'r')

	vals = []	
	# filling columns into independent lists
	for line in file:
		for w in line.rstrip('\t\n').split(" "):
			vals.append(w)
		p_id.append(vals[0])
		s_id.append(vals[1])
		t_id.append(vals[2])
		#b_start.append(vals[3])
		#b_end.append(vals[4])
		#wsp_after.append(vals[5])
		h_id.append(vals[6])
		word.append(vals[7])
		norm_word.append(vals[8])
		#lemma.append(vals[9])
		pos.append(vals[10])
		ner.append(vals[11])
		dep.append(vals[12])
		quote.append(vals[13])
		ch_id.append(vals[14])
		del vals[:]

	return (p_id, s_id, t_id, b_start, b_end, wsp_after, h_id, word,
			 norm_word, lemma, pos, ner, dep, quote, ch_id, character_set_id,
			 character)
# converting strings to ints
def boolean(string):
	if string == 'true':
		return True
	elif string == 'false':
		return False

def fill_vars(p_id, s_id, t_id, b_start, b_end, wsp_after, h_id, word,
				norm_word, lemma, pos, ner, dep, quote, ch_id, 
				character_set_id, character):
	 
	
	p_id = [int(i) for i in p_id[1:]]
	s_id = [int(i) for i in s_id[1:]]
	t_id = [int(i) for i in t_id[1:]]
	#b_start = [int(i) for i in b_start[1:]]
	#b_end = [int(i) for i in b_end[1:]]
	#wsp_after = wsp_after[1:]
	h_id = [int(i) for i in h_id[1:]]
	word = word[1:]
	norm_word = norm_word[1:]
	#lemma = lemma[1:]
	pos = pos[1:]
	ner = ner[1:]
	dep = dep[1:]
	quote = [boolean(i) for i in quote[1:]]
	ch_id = [int(i) for i in ch_id[1:]]	
	character_set_id = sorted(set(ch_id)) # set of sorted character ids

	# initializing dictionary character with empty values
	for i in range(len(character_set_id)):
		character[character_set_id[i]] = set({})

	return (p_id, s_id, t_id, b_start, b_end, wsp_after, h_id, word,
			 norm_word, lemma, pos, ner, dep, quote, ch_id, character_set_id,
			 character)
	
# creating a dictionary of characters mapped by their ids
def map_characters(character):
	#name_file = open('/home/nikhil/Documents/Project/character_names.txt',\
	#				'r')
	name_file = open('C:/Users/Nikhil Prabhu/Documents/Programming/Project/character_names.txt', 'r')

	for line in name_file:
		vals = []
		for w in line.rstrip('\n').split("\t"):
			vals.append(w)
		char_ID = int(vals[1]) 
		char_names = vals[2]
		for name in char_names.split("/"):
			character[char_ID].add(name)
	del character[-1]

def relative_head(tok, token_list_num):
	if tok == -1:
		return tok
	else:
		return tok - min(token_list_num)

def define_lists(sentence_token, t_id, h_id, word, norm_word, pos, ner, dep,
				 ch_id, quote, token_list, htoken_list, word_list,
				 norm_word_list, pos_list, ner_list, dep_list, ch_id_list,
				 quote_list, norm_tok_list, norm_htok_list, all_quotes):
	
	for num in range(max(sentence_token)):
		token_list[num] = ([t_id[i] for i in range(sentence_token[num],
							sentence_token[num+1])])

		htoken_list[num] = ([h_id[i] for i in range(sentence_token[num],
							sentence_token[num+1])])

		word_list[num] = ([word[i] for i in range(sentence_token[num],
							sentence_token[num+1])])

		norm_word_list[num] = ([norm_word[i] for i in 
								range(sentence_token[num], 
								sentence_token[num+1])])

		pos_list[num] = ([pos[i] for i in range(sentence_token[num],
						 sentence_token[num+1])])

		ner_list[num] = ([ner[i] for i in range(sentence_token[num],
						 sentence_token[num+1])])

		dep_list[num] = ([dep[i] for i in range(sentence_token[num],
						 sentence_token[num+1])])

		ch_id_list[num] = ([ch_id[i] for i in range(sentence_token[num],
							 sentence_token[num+1])])

		quote_list[num] = ([quote[i] for i in range(sentence_token[num],
							 sentence_token[num+1])])
		
	for num in range(max(sentence_token)):
		norm_tok_list[num] = ([tok - min(token_list[num])
								for tok in token_list[num]])
		norm_htok_list[num] = ([relative_head(tok, token_list[num])
							 	for tok in htoken_list[num]])

	for num in range(max(sentence_token)):
		if any([quote[i] == True for i in range(sentence_token[num],
				sentence_token[num+1])]):
			all_quotes.add(num)

	return (token_list, htoken_list, word_list,
			norm_word_list, pos_list, ner_list, dep_list, ch_id_list,
			 quote_list, norm_tok_list, norm_htok_list, all_quotes)

def get_sentence_tokens(word, sentence_token):
	#sent_file = open('/home/nikhil/Documents/Project/sentence_tokens.txt',\
	#				'r')
	sent_file = open('C:/Users/Nikhil Prabhu/Documents/Programming/Project/sentence_tokens.txt', 'r')
	for line in sent_file:
		vals = []
		for w in line.rstrip('\n').split("\t"):
			vals.append(w)
		sent_ID = int(vals[0]) 
		token_ID = int(vals[1])
		sentence_token[sent_ID] = token_ID
	sentence_token[max(sentence_token)+1] = len(word)	

	return sentence_token
	
def write_pickle(pickle, p_id, s_id, t_id, b_start, b_end, wsp_after, h_id,
				 word, norm_word, lemma, pos, ner, dep, quote, ch_id, 
				 character_set_id, character, sentence_token, token_list,
				 htoken_list, word_list, norm_word_list, pos_list, ner_list, 
				 dep_list, ch_id_list, quote_list, norm_tok_list, norm_htok_list,
				 all_quotes):
	variable = {}
	variable['character'] = character
	variable['p_id'] = p_id
	variable['s_id'] = s_id
	variable['t_id'] = t_id
	#variable['b_start'] = b_start
	#variable['b_end'] = b_end
	#variable['wsp_after'] = wsp_after
	variable['h_id'] = h_id
	variable['word'] = word
	variable['norm_word'] = norm_word
	#variable['lemma'] = lemma
	variable['pos'] = pos
	variable['ner'] = ner
	variable['dep'] = dep
	variable['quote'] = quote
	variable['ch_id'] = ch_id
	variable['sentence_token'] = sentence_token
	#variable['character_occurences'] = character_occurences
	#variable['sentence_graph'] = sentence_graph
	variable['token_list'] = token_list
	variable['htoken_list'] = htoken_list
	variable['norm_tok_list'] = norm_tok_list
	variable['norm_htok_list'] = norm_htok_list
	variable['word_list'] = word_list
	variable['norm_word_list'] = norm_word_list
	variable['pos_list'] = pos_list
	variable['ner_list'] = ner_list
	variable['dep_list'] = dep_list
	variable['ch_id_list'] = ch_id_list
	variable['quote_list'] = quote_list
	variable['all_quotes'] = all_quotes

	with open('variable.pkl', 'wb') as fp:
		pickle.dump(variable, fp, pickle.HIGHEST_PROTOCOL)
