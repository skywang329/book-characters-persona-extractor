from tuple_methods import *
from wordnet_methods import *
from string_methods import *
from print_methods import *
from dict_methods import *
##############################################################################
##############################################################################
##############################################################################
#################### LIST METHODS ############################################
##############################################################################
##############################################################################
##############################################################################
##############################################################################

def bigger(li1, li2):
	return li1 if len(li1) > len(li2) else li2

def parent(parse_tree, tup, i):
	return parse_tree[i][parent_index(tup)]

def is_ancestor(parse_tree, tup1, tup2, i):
	if parent_index(tup1) == -1:
		return False
	elif is_parent(tup1, tup2):
		return True
	else:
		return is_ancestor(parse_tree, parent(parse_tree, tup1, i), tup2, i)

def has_VB_in_path(parse_tree, tup1, tup2, i):
	if not is_ancestor(parse_tree, tup1, tup2, i):
		return False
	elif tup1 == tup2:
		return False
	elif is_pos_of(tup1, "VB"):
		return True
	else:
		return has_VB_in_path(parse_tree, 
							  parent(parse_tree, tup1, i),
							  tup2, 
							  i)

def is_a_be_or_have(tup, bes, haves):	
	return is_norm_word_of_any(tup, (bes+haves))

def is_g_nibling(parse_tree, tup1, tup2, i):
	return (is_ancestor(parse_tree, tup1, parent(parse_tree, tup2, i), i) and 
			not is_ancestor(parse_tree, tup1, tup2, i))


def count_people(people):
	return len(set([char_id(tup) for tup in people]))

def get_people(parse_tree, i):
	return [tup for tup in parse_tree[i] if is_person(tup)]

def get_nsubj_people(parse_tree, i):
	people = sorted([tup for tup in parse_tree[i] if 
			  		 is_dependency_of(tup, "nsubj") and 
			  		 is_person(tup)])
	
	return people
	
def get_adjectives(parse_tree, i):
	return [tup for tup in parse_tree[i] if is_adjective(tup)]

def get_nmod_tup(parse_tree, word, a, li, i):
	return ([tup for tup in parse_tree[i] if 
			is_lower_word_equal(tup, word) and
			(any(is_parent(tup, x) for x in li) or 
			 is_parent(tup, a))])

def is_subset(li1, li2):
	return set(li1) <= set(li2)

def is_substring(s1, s2):
	return s1 in s2
	
def superset(li1, li2):
	if is_subset(li1, li2):
		return li2
	else:
		return li1

def filter_duplicates(li):
	return sorted(list(set(li)))

def all_words_in_between(parse_tree, li, i):
	if li:
		start = li[0][0]
		end = li[-1][0]+1
		
		index_range = range(start, end)
		list_indices = [index(word) for word in li]
		
		if [r_index for r_index in index_range if r_index not in list_indices]:
			return sorted([word for word in parse_tree[i]
							if index(word) in index_range])
	
	return li

def remove_stop_words(li, stopwords):
	if li:
		if li[0][5] in stopwords:
			li = li[1:]
		if li:
			if li[-1][5] in stopwords:
				li = li[:-1]

	return li


def find_parent_and_prev_negs(parse_tree, adj_list, p, a, i, people, conjunctions):
	def parent_negs(parse_tree, li, i):
		return ([tup for tup in parse_tree[i] if 
				is_dependency_equal(tup, "neg") and
		 		any(is_parent(tup, x) for x in li) and
		 		tup not in li])

	def prev_negs(parse_tree, li, p, a, i, people, conjunctions):
		def not_first_person(tup, li):
			def prev_person_is_same(li, tup):
				if previous_item_exists(li, tup):
					return char_id(tup) == char_id(previous_item(li, tup))

				return False

			if tup in li:
				return (li.index(tup) != 0 and 
						not prev_person_is_same(li, tup))
			
			return False

		return ([tup for tup in parse_tree[i] if 
				is_dependency_equal(tup, "neg")
		 		and parse_tree[i].index(tup) < parse_tree[i].index(a)
		  		and no_conj_in_between(parse_tree, tup, a, p, i, conjunctions) and
		  		no_punct_in_between(parse_tree, tup, a, p, i, conjunctions) and
		  		tup not in li if 
		  		not not_first_person(p, people)])

	return (parent_negs(parse_tree, adj_list, i) +
			prev_negs(parse_tree, adj_list, p, a, i, people, conjunctions))


def is_near_word_JJ_or_RB(parse_tree, tup, i, k):
	if near_word_exists(parse_tree, tup, i, k):
		return is_pos_of_any(near_word(parse_tree, tup, i, k), ["JJ", "RB"])
	
	return False

def is_prev_word_a_be_or_have(parse_tree, tup, i, bes, haves):
	if prev_word_exists(parse_tree, tup, i):
		return is_a_be_or_have(prev_word(parse_tree, tup, i), bes, haves)
	
	return False

def is_prev_of_id(parse_tree, tup1, tup2, i):
	if prev_word_exists(parse_tree, tup2, i):
		return char_id(prev_word(parse_tree, tup2, i)) == char_id(tup1)
			
	return False

def next_word_had_or_is_conditions(parse_tree, p, i, bes, haves):
	if next_word_exists(parse_tree, p, i):
		next = next_word(parse_tree, p, i)
		if is_word_equal(next, ["is", "had", "has"]):
			return is_root(next) or not is_pos_of(parent(parse_tree, next, i), "VB")

	return False

def is_next_of_id(parse_tree, tup1, tup2, i):
	if next_word_exists(parse_tree, tup1, i):
		return char_id(next_word(parse_tree, tup1, i)) == char_id(tup2)

	return False

def is_next_word_conj(parse_tree, tup, i, conjunctions):
	if next_word_exists(parse_tree, tup, i):
		return word(next_word(parse_tree, tup, i)) in conjunctions

	return False

def is_next_word_comma(parse_tree, tup, punctuation, i):
	if next_word_exists(parse_tree, tup, i):
		return is_word_equal(next_word(parse_tree, tup, i), ",")

	return False

def is_next_to_next_word_another_person(parse_tree, tup, p, i):
	if near_word_exists(parse_tree, tup, i, 2):
		id = char_id(near_word(parse_tree, tup, i, 2))
		return id != -1 and id != char_id(p)

	return False

def is_prev_word_a_person(parse_tree, tup, i):
	if prev_word_exists(parse_tree, tup, i):
		return char_id(prev_word(parse_tree, tup, i)) != -1

	return False

def find_nearby_vbs(parse_tree, tup, i, vb_strings):
	vibs = []
	
	if prev_word_exists(parse_tree, tup, i):
		prev = prev_word(parse_tree, tup, i)
		if (is_pos_equal_any(prev, vb_strings)):
			vibs.append(prev)
	if next_word_exists(parse_tree, tup, i):
		next = next_word(parse_tree, tup, i)
		if (is_pos_equal_any(next, vb_strings)):
			vibs.append(next)
	
	return vibs

def add_prevs_of_negs(parse_tree, negs, i):
	prevs = []
	for neg in negs:
		if prev_word_exists(parse_tree, neg, i):
			prev = prev_word(parse_tree, neg, i)
			if (has_common_parent(prev, neg) and 
				not is_dependency_equal(prev, "punct")):
				prevs.append(prev)
	
	return negs + prevs

def have_condition(parse_tree, p, i, conjunctions):
	return [tup for tup in parse_tree[i] if is_word_equal(tup, "have") and 
			(is_g_nibling(parse_tree, tup, p, i) or is_ancestor(parse_tree, tup, p, i)) and 
			is_pos_of(parent(parse_tree, p, i), "VB") and 
			no_punct_in_between(parse_tree, tup, p, p, i, conjunctions)]	

def surrounding_words_linked(parse_tree, tup, i):
	return (
			(
			 is_near_word_JJ_or_RB(parse_tree, tup, i, -1) and
			 is_near_word_JJ_or_RB(parse_tree, tup, i, 1)
			) or 
			(
			 have_same_dependency(prev_word(parse_tree, tup, i),
							   	  next_word(parse_tree, tup, i))
			)
		   )

def descriptive_comma(parse_tree, tup, p, i, conjunctions):
	return	(
			 is_word_equal(tup, ",") and			 
			 (is_dependency_of_any(next_word(parse_tree, tup, i), ["amod", "conj", "advcl"]) or
			  (is_word_equal_any(next_word(parse_tree, tup, i), 
			 	 						   conjunctions) and 
			   is_near_word_JJ_or_RB(parse_tree, tup, i, 2)
			  ) or 
			  is_next_of_id(parse_tree, tup, p, i)
			 ) 
			)
		   

def remove_invalid_splitters(parse_tree, li, p, i, conjunctions):
	return [tup for tup in li if 
			not surrounding_words_linked(parse_tree, tup, i) and 
			not descriptive_comma(parse_tree, tup, p, i, conjunctions)]

def remove_linking_splitters(parse_tree, li, p, i, conjunctions):
	return [tup for tup in li if 
			not surrounding_words_linked(parse_tree, tup, i)]


def find_as(parse_tree, li, i):
	def is_there_one_as(parse_tree, li, i):
		as_words = [tup for tup in li if is_word_equal(tup, "as")]
		if len(as_words) == 1:
			return parse_tree[i].index(as_words[0])
		
		return -1

	first_as = is_there_one_as(parse_tree, li, i)
	if first_as != -1:
		second_as = is_there_one_as(parse_tree, parse_tree[i][first_as+1:], i)
		if second_as != -1:
			second_as_tup = parse_tree[i][second_as]
			return [second_as_tup, parent(parse_tree, second_as_tup,i)]
	
	return []


def find_punctuations(parse_tree, li, i):
	#assumes list is sorted
	indices = range(li[0][0], li[-1][0])
	puncts = ([tup for tup in parse_tree[i] if 
			  is_dependency_equal(tup, "punct") and 
			  index(tup) in indices])
	if not (len(puncts) == 2 and is_same_norm_word(puncts[0], puncts[1])):
		return puncts
	else:
		return []

##############################################################################
##############################################################################
##############################################################################
#################### ADJECTIVE METHODS #######################################
##############################################################################
##############################################################################
##############################################################################
##############################################################################

def has_direct_dependency(parse_tree, a, i):
	return not is_dependency_of_any(a, ["det", "case"])


def find_advmods_and_dets(parse_tree, a, i, bes, haves):
	return ([tup for tup in parse_tree[i] if
			is_dependency_equal_any(tup, ["advmod", "det"]) and 
			(has_common_parent(tup, a) or 
			is_parent(tup, a)) and 
			tup != a and
			is_prev_word_a_be_or_have(parse_tree, tup, i, bes, haves)]) 


def find_RBs(parse_tree, a, i):
	return	([tup for tup in parse_tree[i] if 
			 is_adverb(tup) and
			 is_parent(tup, a)])

def find_valid_adj_parents(parse_tree, p, a, i, conjunctions):
	def add_parent_of_adj_conds(parse_tree, a, i):
		return is_dependency_of_any(a, 
									["nmod:", "conj:", "xcomp", 
									 "dobj", "amod", "advmod"]
									)

	parent_tup = parent(parse_tree, a, i)

	if (add_parent_of_adj_conds(parse_tree, a, i) and 
		no_punct_in_between(parse_tree, a, parent_tup, p, i, conjunctions) and 
		no_conj_in_between(parse_tree, a, parent_tup, p, i, conjunctions)):
		return [parent_tup]
	else:
		return []

def find_preps(parse_tree, a, i):
	return ([tup for tup in parse_tree[i] if 
			is_pos_equal(tup, "IN") and
	 		not is_dependency_equal(tup, "mark") and 
	 		is_parent(tup, a)])

def get_trait_advmods(parse_tree, a, i):
	return ([tup for tup in parse_tree[i] if 
			is_dependency_equal(tup, "advmod") and 
			is_parent(tup, a) and 
			tup != a])

def find_adj_advcls(parse_tree, a, i):
	return ([tup for tup in parse_tree[i] if 
			is_dependency_equal(tup, "advcl") and 
			is_adjective(tup) and 
			(is_parent(tup, a) or
			has_common_parent(tup, a)) and 
			tup != a])

def find_adj_acl_relcls(parse_tree, p, i):
	return ([tup for tup in parse_tree[i] if 
			is_dependency_equal(tup, "acl:relcl") and 
			is_adjective(tup) and 
			(is_parent(tup, p) or
			has_common_parent(tup, p)) and 
			tup != p])
	
def check_for_in(parse_tree, p, a, i, conjunctions):
	def get_in_words(parse_tree, p, a, i):
		return ([tup for tup in parse_tree[i] if 
				is_word_equal(tup, "in") and 
				parse_tree[i].index(tup) < parse_tree[i].index(a) and 
				parse_tree[i].index(p) < parse_tree[i].index(tup)])

	in_words = get_in_words(parse_tree, p, a, i)
	if in_words:
		word = sorted(in_words)[-1]
		return (no_conj_in_between(parse_tree, word,
								   a, p, i, conjunctions) and 
				no_punct_in_between(parse_tree, word, a, p, i, conjunctions))
	
	return False

def no_punct_in_between(parse_tree, tup1, tup2, p, i, conjunctions):
	return not (remove_invalid_splitters(parse_tree, 
									 find_punctuations(
									 				  parse_tree, 
									 				  all_words_in_between
									 				  	(
									 				  	 parse_tree, 
									 				  	 sorted([tup1, tup2]), 
									 				  	 i
									 				  	), 
									 				  i
									 				 ), 
									 p,
									 i,
									 conjunctions
									)
			   )

def no_conj_in_between(parse_tree, tup1, tup2, p, i, conjunctions):
	def get_conjunctions(parse_tree, li, i, conjunctions):
		#assumes list is sorted
		indices = range(li[0][0], li[-1][0])
		return ([tup for tup in parse_tree[i] if 
				word(tup) in conjunctions
		 		and index(tup) in indices])

	return not (remove_linking_splitters(parse_tree,
										 get_conjunctions(
										 				  parse_tree, 
									 					  all_words_in_between
									 					  	(
									 					  	 parse_tree, 
									 					  	 sorted([tup1, tup2]),
									 					  	 i
										 				  	), 
										 				  i, 
										 				  conjunctions
										 				 ), 
										 p,
										 i,
										 conjunctions
										 ) 
				)
	
def near_word_exists(parse_tree, tup, i, k):
	return (index(tup) + k >= 0 and index(tup) + k < len(parse_tree[i]))

def next_word_exists(parse_tree, tup, i):
	return near_word_exists(parse_tree, tup, i, 1)

def prev_word_exists(parse_tree, tup, i):
	return near_word_exists(parse_tree, tup, i, -1)

def near_word(parse_tree, tup, i, k):
	return parse_tree[i][index(tup) + k]

def next_word(parse_tree, tup, i):
	return parse_tree[i][index(tup) + 1]

def prev_word(parse_tree, tup, i):
	return parse_tree[i][index(tup) - 1]

def words_between_adj_and_parent(parse_tree, a, i):
	if index(a) < parent_index(a):
		indices = range(index(a) + 1, parent_index(a) + 1)
	else:
		indices = range(parent_index(a), index(a))

	tups = [tup for tup in parse_tree[i] if index(tup) in indices]
	
	return sorted(tups)

def punct_split(parse_tree, li, p, a, i, conjunctions):
	bigl = []
	phrase = []
	last = 0
	
	puncts = remove_invalid_splitters(parse_tree, 
									  [word for word in li if is_dependency_equal(word, "punct")],
									  p, i,
									  conjunctions)

	for punct in puncts:
		if True:	
			bigl.append(li[last:li.index(punct)])
			last = li.index(punct) + 1
	bigl.append(li[last:])


	for sublist in bigl:
		if (a in sublist or 
			sublist_follows_p(parse_tree, p, i, sublist) or 
			is_first_word_person(sublist, p)
		   ):
			phrase += sublist
	
	return phrase

def is_first_word_person(li, p):
	if li :
		return char_id(li[0]) == char_id(p)
	
	return False

def sublist_follows_p(parse_tree, p, i, sublist):
	if sublist and p and next_word_exists(parse_tree, p, i):
		return next_word(parse_tree, p, i) == sublist[0]
	
	return False

def sibling_states_conditions(parse_tree, p, a, i):
	return (			
			not (is_dependency_of(a, "dep")) and
			not (is_dependency_of(a, "nmod") and
				 not is_adjective(parent(parse_tree, a, i))
			 	) and
			not ([tup for tup in parse_tree[i] if 
				  is_dependency_of(tup, "nsubj") and 
				  is_parent(tup, a)])
	  		)

def find_conj_and_nmod_words(parse_tree, a, i):
	def get_nmod_children(parse_tree, a, i):
		return (
				[tup for tup in parse_tree[i] if 
				 is_dependency_of(tup, "nmod:") and 
				 (
				  is_parent(tup, a) or
				  has_common_parent(tup, a) or 
			 	  tup == a or 
			 	  tup == parent(parse_tree, a, i))]
			   )

	def get_conj_children(parse_tree, a, i):
		return (
				[tup for tup in parse_tree[i] if 
				is_dependency_of(tup, "conj:") and 
				not (
					 is_pos_equal(tup, "VBD") or 
					 is_pos_equal(tup, "VB")
					 ) and
				(
				 is_parent(tup, a) or 
				 has_common_parent(tup, a) or
				 tup == a or 
				 tup == parent(parse_tree, a, i))]
				)

	nmod_list = []
	conj_list = []

	def get_words(parse_tree, li, a, string, i):
		tuples = []
		for tup in li:
			word = dep(tup).split(string)[1].lower()
			if '_' in word:
				split_word = word.split("_")
				first_mods = get_nmod_tup(parse_tree, split_word[0], a, li, i)
				tuples += first_mods
				tuples += get_nmod_tup(parse_tree, split_word[1], a, first_mods,
									   i)
			else:
				nmod_tup = get_nmod_tup(parse_tree, word, a, li, i)
				if nmod_tup:
					tuples += nmod_tup
				else:
					li.remove(tup)
				
		return tuples

	nmod_children = get_nmod_children(parse_tree, a, i)
	nmod_list += (get_words(parse_tree, nmod_children, a, "nmod:", i) + 
				  nmod_children)
	conj_children = get_conj_children(parse_tree, a, i)
	conj_list += (get_words(parse_tree, conj_children, a, "conj:", i) + 
				  conj_children)
	
	return nmod_list + conj_list

##############################################################################
##############################################################################
##############################################################################
#################### ADJ_LIST METHODS ########################################
##############################################################################
##############################################################################
##############################################################################
##############################################################################


def find_latter_preps_and_coord_conjs(parse_tree, adj_list, p, a, i):
	def is_present_before(parse_tree, tup, li, i):
		return parse_tree[i].index(tup) < li[0][0]	

	def ins(parse_tree, p, a, i):
		return ([tup for tup in parse_tree[i] if 
				is_pos_equal(tup, "IN")
		 		and not is_dependency_equal(tup, "mark") and
		 		not is_present_before(parse_tree, tup, sorted([p, a]), i) and
		 		(has_common_parent(tup, a) or 
		 		is_parent(tup, a))])
		
	def ccs(parse_tree, adj_list, p, a, i):
			return ([tup for tup in parse_tree[i] if 
					is_pos_equal(tup, "CC") and
					not is_present_before(parse_tree, tup, sorted([p, a]), i) and
					(any(is_parent(tup, x) for x in adj_list) or 
			 		is_parent(tup, a) or has_common_parent(tup, a))])

	return ins(parse_tree, p, a, i) + ccs(parse_tree, adj_list, p, a, i)

def nsubj_children(parse_tree, p, a, i, conjunctions):
	return (
			[
			 tup for tup in parse_tree[i] if 
			 is_dependency_of(tup, "nsubj") and 
			 (is_parent(tup, a) or 
			  (
			   is_pos_of(parent(parse_tree, a, i), "VB") and 
			   is_related(tup, parent(parse_tree, a, i))
			   and not (no_punct_in_between(parse_tree, p, tup, p, i, conjunctions)
			   			and parse_tree[i].index(tup) > parse_tree[i].index(p))
			  )
			 ) and
			 char_id(tup) != -1 and 
			 (char_id(tup) != char_id(p) and 
			  not (
			  	   (is_dependency_of(tup, "conj") and is_parent(tup, p)) or 
			 	   (is_dependency_of(p, "conj") and is_parent(p, tup))
			 	  )
			 )
			]
		   )

def nsubj_parents(parse_tree, p, a, i):
	return ([tup for tup in parse_tree[i] if 
			is_dependency_of(tup, "nsubj") and 
			is_parent(p, tup) and 
			char_id(tup) != char_id(p)])

def tup_is_before(parse_tree, li, tup, i):
	return parse_tree[i].index(tup) < parse_tree[i].index(sorted(li)[0])
	
def recursively_add_all_dep_and_pos_children(parse_tree, dep_strings, 
											 pos_strings, adj_list, i):
	def recursively_add_all_dep_and_pos_children(parse_tree, dep_strings, pos_strings, li, filled_li, i):
		def get_the_dep_and_pos_children(parse_tree, dep_strings, pos_strings, li, filled_li, i, deps_and_pos):
			def add_all_dep_and_pos_children(parse_tree, dep_strings, pos_strings, li, filled_li, i):
				return ([tup for tup in parse_tree[i] if 
						(is_dependency_of_any(tup, dep_strings) or 
						is_pos_of_any(tup, pos_strings)) and
						is_parent_in(tup, filled_li) and
						tup not in li])
			
			if li:
				children = add_all_dep_and_pos_children(parse_tree, dep_strings, pos_strings, li, filled_li, i)
				deps_and_pos += children
				return get_the_dep_and_pos_children(parse_tree, 
											dep_strings, 
											pos_strings,
											children, 
											children,
											i, 
											deps_and_pos)
			
			return deps_and_pos
	
		return get_the_dep_and_pos_children(parse_tree, dep_strings, pos_strings, li, filled_li, i, deps_and_pos = [])

	descendants = ["do while loop emulator"]
	while descendants:
		descendants = []
		descendants += (recursively_add_all_dep_and_pos_children
							(
						 	 parse_tree, 
						 	 dep_strings,
						 	 pos_strings, 
						 	 adj_list,
						 	 all_words_in_between(parse_tree,
						 						  filter_duplicates(adj_list),
						 						  i),
						 	 i
							))

		adj_list += descendants
		
	return adj_list

def in_in_between_or_root_a(parse_tree, p, a, i, conjunctions):
	return (check_for_in(parse_tree, p, a, i, conjunctions) or 
		  	is_root(a))

def ancestor_states_conditions(parse_tree, p, a, i, conjunctions, bes, haves):
	def parent_of_be_or_have(parse_tree, a, i, bes, haves):
		return ([tup for tup in parse_tree[i] if 
				is_a_be_or_have(tup, bes, haves) and
				is_parent(tup, a)])

	return (not parent_of_be_or_have(parse_tree, a, i, bes, haves) or
			find_nearby_vbs(parse_tree, a, i, ["VBG", "VBD"]) or
			in_in_between_or_root_a(parse_tree, p, a, i, conjunctions))

def add_nt_words(parse_tree, negs, i):
	for neg in negs:
		if is_word_equal(neg, "n't"):
			negs.append(prev_word(parse_tree, neg, i))
	return negs


def add_to_set(word_list, p, a, i, char_id, description, container, facts, states, feelings, invalid, all_phrases):
	if char_id not in container:
		container[char_id] = {}
	
	if i not in container[char_id]:
		container[char_id][i] = []
		container[char_id][i].append(description)
		store_description(word_list, p, a, i, description, container, 
						  facts, states, feelings, invalid, 
						  all_phrases)

	else:
		added = False
		for j in range(len(container[char_id][i])):
			if (is_subset(container[char_id][i][j], description) or
				is_subset(description, container[char_id][i][j])):
				container[char_id][i][j] = superset(container[char_id][i][j], description)
				added = True
		if not added:
			container[char_id][i].append(description)

		subset_phrases = [phrase for phrase in all_phrases if 
						  phrase[0] == i and 0 not in phrase[5] and 
						  (is_substring(phrase[4], get_adj_from_list(description)) or 
						   is_substring(get_adj_from_list(description), phrase[4]))]
		
		if subset_phrases:
			for ph in subset_phrases:
				all_phrases.remove(ph)
				all_phrases.add((ph[0], ph[1], ph[2], ph[3], 
								superset(ph[4], get_adj_from_list(description)), ph[5]))
				
		store_description(word_list, p, a, i, description, container, 
						  facts, states, feelings, invalid, 
						  all_phrases)


def find_non_person_nsubjs(parse_tree, a, i):
	return [tup for tup in parse_tree[i] if 
			is_dependency_equal(tup, "nsubj") and 
			is_parent(tup, a) and char_id(tup) == -1 and 
			not is_pos_of_any(tup, ["PRP", "NNP", "WP", "DT"])]
	
def find_child_sibling_and_between_negs(parse_tree, p, a, i):
	def find_child_sibling_negs(parse_tree, a, i):
		def child_or_sibling_negs(parse_tree, a, i):
			return ([tup for tup in parse_tree[i] if 
					is_dependency_equal(tup, "neg") and
					(is_parent(tup, a) or
					has_common_parent(tup, a))])

		return sorted(add_nt_words(parse_tree, 
								   add_prevs_of_negs(parse_tree, 
											 		 child_or_sibling_negs(parse_tree,
											 				  			 a,
											 					 		 i),
											 		 i),
								   i))

	def find_between_negs(parse_tree, p, a, i):
		return ([tup for tup in parse_tree[i] if 
				 is_dependency_of(tup, "neg") and 
				 index(p) < index(tup) and 
				 index(tup) < index(a)])

	return (find_child_sibling_negs(parse_tree, a, i) + 
			find_between_negs(parse_tree, p, a, i))

def add_dependents(parse_tree, adj_list, people, p, a, i, conjunctions, bes, haves):
	
	if is_dependency_of(a, "xcomp"):
		adj_list += words_between_adj_and_parent(parse_tree, a, i)
	
	adj_list += find_child_sibling_and_between_negs(parse_tree, p, a, i)
			
	adj_list += find_RBs(parse_tree, a, i)	
	adj_list += find_non_person_nsubjs(parse_tree, a, i)

	adj_list += find_nearby_vbs(parse_tree, a, i, ["VBG", "VBD", "VBZ"])
	adj_list += find_nearby_vbs(parse_tree, p, i, ["VBG", "VBD", "VBZ"])
	
	adj_list += find_adj_advcls(parse_tree, a, i)
	adj_list += find_adj_acl_relcls(parse_tree, p , i)
	
	adj_list += find_preps(parse_tree, a, i)
	adj_list += find_advmods_and_dets(parse_tree, a, i, bes, haves)
	adj_list += find_conj_and_nmod_words(parse_tree, a, i)
	
	adj_list += find_valid_person_parents(parse_tree, p, i, conjunctions)	
	adj_list += find_valid_adj_parents(parse_tree, p, a, i, conjunctions)

	adj_list += find_latter_preps_and_coord_conjs(parse_tree, adj_list, p, a, i)
	adj_list += find_punctuations(parse_tree, adj_list, i)
	adj_list += find_as(parse_tree, filter_duplicates(adj_list), i)
	adj_list += find_parent_and_prev_negs(parse_tree, adj_list, p, a, i, people, conjunctions)

	adj_list = recursively_add_all_dep_and_pos_children(parse_tree, 
														 ["xcomp", "ccomp", 
														  "nmod", "conj", 
														  "dobj", "cc", "aux"],
														 ["VB", "RB", "WRB"],
														 adj_list,
														 i)
	
	return adj_list
	
def refine(parse_tree, adj_list, p, a, i, stopwords, conjunctions):

	adj_list = all_words_in_between(parse_tree, filter_duplicates(adj_list), i)
	
	adj_list = punct_split(parse_tree, all_words_in_between(parse_tree, 
															adj_list, 
															i), 
						   p, a, i, conjunctions)

	adj_list = all_words_in_between(parse_tree, filter_duplicates(adj_list), i)	
	adj_list = remove_stop_words(adj_list, stopwords)

	return filter_duplicates(adj_list)


def find_valid_person_parents(parse_tree, p, i, conjunctions):
	def add_parent_of_person_conds(parse_tree, p, i):
		return (is_pos_of(parent(parse_tree, p, i), "VB"))

	parent_tup = parent(parse_tree, p, i)

	if (add_parent_of_person_conds(parse_tree, p, i) and 
		no_punct_in_between(parse_tree, p, parent_tup, p, i, conjunctions)):
		return [parent_tup]
	
	return []

def get_description(parse_tree, people, p, a, i, stopwords, conjunctions, bes, haves):
	adj_list = add_dependents(parse_tree, [a], people, p, a, i, conjunctions, bes, haves)		
	adj_list = refine(parse_tree, filter_duplicates(adj_list), p, a, i, 
					  stopwords, conjunctions)

	return adj_list	

##############################################################################
##############################################################################
##############################################################################
#################### PRINT METHODS ###########################################
##############################################################################
##############################################################################
##############################################################################
##############################################################################

def print_sentence_and_tuples(parse_tree, word_list, (p, a, i, facts)):
	print i, '--\n', sentence(word_list, i), '\n', parse_tree[i],\
	 '----------------------\n'
	print p
	print a
	print parent(parse_tree, a, i)
	print parent(parse_tree, p, i)
	print '-----------------------------------------------------------\
	-----------------\n'

def print_in_string(dictionary):
	stringed_dict = {}
	for key in dictionary:
		stringed_dict[key] = get_adj_from_list(dictionary[key])

	return stringed_dict

def store_description(word_list, p, a, i, description, dictionary, facts, states, feelings, invalid, all_phrases):
	desc_num = []
	if dictionary == invalid:
		desc_num.append(0)
	if dictionary == facts:
		desc_num.append(1)
	elif dictionary == states:
		desc_num.append(2)
	elif dictionary == feelings:
		desc_num.append(3)
	
	same_phrases = [phrase for phrase in all_phrases if phrase[0] == i and 
					phrase[4] == get_adj_from_list(description) and 
					desc_num[0] != 0 and 0 not in phrase[5] and desc_num[0] not in phrase[5]]
	if same_phrases:
		for tag in [phrase[5] for phrase in same_phrases]:
			for val in tag:
				if val not in desc_num:
					desc_num.append(val)

	for phrase in same_phrases:
		all_phrases.add((phrase[0], phrase[1], phrase[2], phrase[3], phrase[4], tuple(desc_num)))
		all_phrases.remove(phrase)

		
	all_phrases.add((i, highlighted_sentence(word_list, i, index(p), index(a)), 
					(index(p), word(p)), (index(a), word(a)), 
					get_adj_from_list(description), tuple(desc_num)))

def print_undifferentiated_personas(descriptions, character):
	describers = descriptions[0]

	facts = describers[0]
	states = describers[1]
	feelings = describers[2]

	#invalid = describers[3]

	for id in sorted(character):
		if id in facts or id in feelings or id in states:
			print'____________________________________________________________'
			print id, sorted(character[id])
			print '----------------'
			print 'FACTS'
			print '----------------'
			if id in facts:
				for sentID in sorted(facts[id]):
					for li in facts[id][sentID]:
						#print sentID, get_adj_from_list(li)
						print get_adj_from_list(li)
			print '----------------'
			print 'STATES'		
			print '----------------'
			if id in states:
				for sentID in sorted(states[id]):
					for li in states[id][sentID]:
						#print sentID, get_adj_from_list(li)
						print get_adj_from_list(li)
			print '----------------'
			print 'FEELINGS'		
			print '----------------'
			if id in feelings:
				for sentID in sorted(feelings[id]):
					for li in feelings[id][sentID]:
						#print sentID, get_adj_from_list(li)
						print get_adj_from_list(li)
			####
			#print '----------------'
			#print 'INVALID'		
			#print '----------------'
			#if id in invalid:
			#	for sentID in sorted(invalid[id]):
			#		print sentID, get_adj_from_list(invalid[id][sentID])
			####
			print'____________________________________________________________'

def print_personas(descriptions, character, differentiated):
	describers = descriptions[0]
	opinion_describers = descriptions[1]

	#print "diff", differentiated
	if not differentiated:
		print_undifferentiated_personas(descriptions, character)
		return

	facts = describers[0]
	states = describers[1]
	feelings = describers[2]

	opinion_facts = opinion_describers[0]
	opinion_states = opinion_describers[1]
	opinion_feelings = opinion_describers[2]

	#invalid = describers[3]

	for id in sorted(character):
		if id in facts or id in feelings or id in states:
			print'____________________________________________________________'
			print id, sorted(character[id])
			print '----------------'
			print 'FACTS'
			print '----------------'
			if id in facts:
				for sentID in sorted(facts[id]):
					for li in facts[id][sentID]:
						#print sentID, get_adj_from_list(li)
						print get_adj_from_list(li)
			print '----------------'
			print 'STATES'		
			print '----------------'
			if id in states:
				for sentID in sorted(states[id]):
					for li in states[id][sentID]:
						#print sentID, get_adj_from_list(li)
						print get_adj_from_list(li)
			print '----------------'
			print 'FEELINGS'		
			print '----------------'
			if id in feelings:
				for sentID in sorted(feelings[id]):
					for li in feelings[id][sentID]:
						#print sentID, get_adj_from_list(li)
						print get_adj_from_list(li)
			####
			#print '----------------'
			#print 'INVALID'		
			#print '----------------'
			#if id in invalid:
			#	for sentID in sorted(invalid[id]):
			#		print sentID, get_adj_from_list(invalid[id][sentID])
			####
		if id in opinion_facts or id in opinion_feelings or id in opinion_states:
			print'____________________________________________________________'
			print id, sorted(character[id])
			print '----------------'
			print 'OPINION FACTS'
			print '----------------'
			if id in opinion_facts:
				for sentID in sorted(opinion_facts[id]):
					for li in opinion_facts[id][sentID]:
						#print sentID, get_adj_from_list(li)
						print get_adj_from_list(li)
			print '----------------'
			print 'OPINION STATES'		
			print '----------------'
			if id in opinion_states:
				for sentID in sorted(opinion_states[id]):
					for li in opinion_states[id][sentID]:
						#print sentID, get_adj_from_list(li)
						print get_adj_from_list(li)
			print '----------------'
			print 'OPINION FEELINGS'		
			print '----------------'
			if id in opinion_feelings:
				for sentID in sorted(opinion_feelings[id]):
					for li in opinion_feelings[id][sentID]:
						#print sentID, get_adj_from_list(li)
						print get_adj_from_list(li)
			####
			#print '----------------'
			#print 'INVALID'		
			#print '----------------'
			#if id in invalid:
			#	for sentID in sorted(invalid[id]):
			#		print sentID, get_adj_from_list(invalid[id][sentID])
			####
			print'____________________________________________________________'
			print'____________________________________________________________'

def print_sample_phrases(all_phrases, pprint, random):
	pp = pprint.PrettyPrinter(indent = 4)
	length = len(all_phrases)
	
	for phrase in random.sample(all_phrases, length/5):
		print '------------'
		print phrase[0]
		print phrase[1], phrase[2]
		print phrase[4]
		print phrase[5]
		print '------------'

def print_valid_phrases(all_phrases, pprint):
	pp = pprint.PrettyPrinter(indent = 4)
	length = len(all_phrases)
	
	for phrase in sorted(all_phrases):
		if phrase[5] != 0:
			print '------------'
			print phrase[0]
			print phrase[1] 
			print phrase[2], phrase[3]
			print phrase[4]
			print phrase[5]
			print '------------'

def print_phrases(all_phrases, pprint):
	pp = pprint.PrettyPrinter(indent = 4)
	length = len(all_phrases)
	
	for phrase in sorted(all_phrases):
		#print '------------'
		#print phrase[0]
		#print phrase[1] 
		#print phrase[2], phrase[3]
		print phrase[4], phrase[2], phrase[3], phrase[5]
		#print '------------'
	#pp.pprint(all_phrases)

def print_all_chars(describers, character):
	
	facts = describers[0]
	states = describers[1]
	feelings = describers[2]
	invalid = describers[3]

	print'____________________________________________________________'
	print 'FACTS'
	print'____________________________________________________________'

	for id in facts:
		print id, sorted(character[id]), '---'
		for sentID in facts[id]:
			print sentID, get_adj_from_list(facts[id][sentID])
		print '------------------------------------'
	print len(facts)

	print'____________________________________________________________'
	print 'STATES'
	print'____________________________________________________________'

	for id in states:
		print id, sorted(character[id]), '---'
		for sentID in states[id]:
			print sentID, get_adj_from_list(states[id][sentID])
		print '------------------------------------'
	print len(states)

	print'____________________________________________________________'
	print 'FEELINGS'
	print'____________________________________________________________'

	for id in feelings:
		print id, sorted(character[id]), '---'
		for sentID in feelings[id]:
			print sentID, get_adj_from_list(feelings[id][sentID])
		print '------------------------------------'
	print len(feelings)

	print'____________________________________________________________'

	print'____________________________________________________________'
	print 'INVALID'
	print'____________________________________________________________'

	for id in invalid:
		print id, sorted(character[id]), '---'
		for sentID in invalid[id]:
			print sentID, get_adj_from_list(invalid[id][sentID])
		print '------------------------------------'
	print len(invalid)

def print_sentence_data(parse_tree, word_list, print_these):
	for tup in print_these:
		print_sentence_and_tuples(parse_tree, word_list, tup)

def get_adj_from_list(adj_list):
	stringed_adjs = []
	adjective = ""
	#for li in adj_list:
	#	adjective = ""
	for item in adj_list:
		if adjective == "":
			if is_word_equal(item, "n't"):
				adjective = 'not'
			elif is_word_equal(item, "'d"):
				adjective = 'had'
			elif (is_word_equal(item, "'s") and 
					not is_pos_equal(item, "POS")):
				adjective = 'is'
			else:
				adjective = word(item)
		else:
			adjective += " " + word(item)
	#stringed_adjs.append(adjective)

	return adjective
	return stringed_adjs

def print_chapters_stuff(chap, chapter_names, chapter_indices, chapter_quote_adjs):
	print "chap", chap, chapter_names[chap], chapter_indices[chap]
	print chapter_adjs[chap].keys()
	print chapter_quote_adjs[chap].keys()
	print len(chapter_names)
	print len(chapter_indices)				

##############################################################################
##############################################################################
##############################################################################
#################### STRING METHODS ##########################################
##############################################################################
##############################################################################
##############################################################################
##############################################################################


	
##############################################################################
##############################################################################
##############################################################################
#################### CHAPTER METHODS #########################################
##############################################################################
##############################################################################
##############################################################################
##############################################################################

def get_chapters(chapter_names, sentence_token, word_list):
	k = 0
	chapter_indices = []
	for i in range(max(sentence_token)):
		if sentence(word_list, i) == chapter_names[k]:
			chapter_indices.append(i)
			k += 1
		if k >= len(chapter_names):
			break
	return chapter_indices

def chapter_split(dictionary, chapter_indices):
	chapter_dict = [{} for x in chapter_indices]
	chapter_dict.append({})
	
	for key in dictionary:
		added = False
		for index in sorted(chapter_indices, reverse = True):
			if key > index and not added:
				chapter_dict[chapter_indices.index(index)][key]\
				 = dictionary[key]
				added = True
		if not added:
			chapter_dict[0][key] = dictionary[key]
	
	return chapter_dict

##############################################################################
##############################################################################
##############################################################################
#################### POV METHODS #############################################
##############################################################################
##############################################################################
##############################################################################
##############################################################################

def pov_split(dictionary, chapter_indices):
	pov_dict = {}
	
	for key in sorted(dictionary):
		added = False
		for index in sorted(chapter_indices, reverse = True):
			pov_name = ""
			pov_id = -1
			if key > index and not added:
				pov_name = stringify(word_list[index][:-1])
				(pov_characters, pov_id) = get_char_id(pov_name)
				if pov_id not in pov_dict:
					pov_dict[pov_id] = {}
				pov_dict[pov_id][key] = dictionary[key]
				added = True
			if pov_id not in person_indices:
				person_indices[pov_id] = []
			if index not in person_indices[pov_id]:	
				person_indices[pov_id].append(index)
				
		
	return (pov_dict, person_indices, pov_characters)

def get_char_id(name):
	for key in sorted(character):
		if title_case(name) in character[key]:
			pov_characters.add(key)
			return (pov_characters, key)
	for key in sorted(character):
		for key_name in character[key]:
			if title_case(name) in key_name:
				pov_characters.add(key)
				return (pov_characters, key)		
	return (pov_characters, -1)

##############################################################################
##############################################################################
##############################################################################
#################### QUOTE METHODS ###########################################
##############################################################################
##############################################################################
##############################################################################
##############################################################################


def append_quotes(parse_tree):
	#quote_file = open('/home/nikhil/Documents/Project/quote_attributions.txt',
	#					'r')
	#quote_file = open('mnt/c/Users/Nikhil Prabhu/Documents/Programming/Project/quote_attributions.txt', 'r')
	quote_file = open('C:/Users/Nikhil Prabhu/Documents/Programming/Project/quote_attributions.txt', 'r')
	quote_adjs = {}
	quote_set = []
	for line in quote_file:
		vals = []
		for w in line.rstrip('\n').split("\t"):
			vals.append(w)
		quote_sentID = int(vals[3]) 
		q_attrID = int(vals[5])
		quote_speakerID = int(vals[7])

		if q_attrID != 0 and quote_speakerID != -1:
			if has_JJ_and_nsubj(parse_tree[quote_sentID],
			 					quote_sentID):
				quote_set.append((quote_sentID, quote_speakerID))
				quote_adjs[quote_sentID] = parse_tree[quote_sentID]
			
		del vals[:]

	return (quote_set, quote_adjs)

def get_id_quotes(quote_set, quote_adjs, char_id):
	pov_quote_adjs = {}
	for tup in quote_set:
		sent_id = index(tup)
		speaker_id = parent_index(tup)
		if speaker_id == char_id:
			pov_quote_adjs[sent_id] = quote_adjs[sent_id]

	return pov_quote_adjs

##############################################################################
##############################################################################
##############################################################################
#################### DESCRIBER METHODS #######################################
##############################################################################
##############################################################################
##############################################################################
##############################################################################
"""
def merge_describers(d1, d2):
	if d2 == {}:
		return d1

	d3 = ({}, {}, {}, {})
	for i in range(4):
		for charId in d1[i]:
			for val in d1[i][charId]:
				for adj_list in d1[i][charId][val]:
					add_to_set(charId, adj_list, d3[i], val)

		for charId in d2[i]:
			for val in d2[i][charId]:
				for adj_list in d2[i][charId][val]:
					add_to_set(charId, adj_list, d3[i], val)

	return d3
"""

def pov_processing(parse_tree, word_list, character, adjs, quote_adjs, 
				   itertools, stopwords, conjunctions, bes, haves, wn, feels, 
				   print_lines):
	pov_out = pov_split(adjs, chapter_indices)
	(pov_adjs, person_indices, pov_characters) = pov_out
	for person_id in pov_adjs:
		if person_id == -1:
			print "person", "UNKNOWN"
		else:
			print "person", character[person_id]
		print sorted(pov_adjs[person_id].keys())
		print "indices ", sorted(person_indices[person_id])
		print len(pov_adjs)				
		describers = extract_personas(parse_tree, word_list,
									  pov_adjs[person_id], itertools,
								   	  stopwords, conjunctions, bes, haves, wn,
									  feels, print_lines)
		pov_quote_adjs = get_id_quotes(quote_set, quote_adjs, person_id)
		opinion_describers = extract_personas(parse_tree, word_list,
											  pov_quote_adjs, itertools,
											  stopwords, conjunctions, bes, 
											  haves, wn, feels, print_lines)
		all_describers = merge_describers(describers, opinion_describers)
				
	return (describers, {}, all_describers)

def chapter_processing(parse_tree, word_list, character, adjs, quote_adjs, 
				 	   itertools, stopwords, conjunctions, bes, haves, wn, feels, 
					   print_lines):
	chapter_adjs = chapter_split(adjs, chapter_indices)
	chapter_quote_adjs = chapter_split(quote_adjs, chapter_indices)
		
	for chap in range(len(chapter_indices)):
		print_chapters_stuff(chap, chapter_names, chapter_indices,
							 chapter_quote_adjs)
		describers = extract_personas(parse_tree, word_list, 
										 chapter_adjs[chap],
		 								 itertools, stopwords,
		 								 conjunctions, bes, haves, 
		 								 wn, feels,
		 								 print_lines)
		opinion_describers = extract_personas(parse_tree, word_list, 
												 chapter_quote_adjs[chap],
												 itertools, stopwords,
												 conjunctions, bes, haves, 
												 wn, feels, 
												 print_lines)
		all_describers = merge_describers(describers, opinion_describers)
		
	return (describers, opinion_describers, all_describers)

def normal_processing(parse_tree, word_list, character, adjs, quote_adjs, 
				 	  itertools, stopwords, conjunctions, bes, haves, wn, feels, 
					  print_lines, differentiated):

	if differentiated:
		opinion_describers, all_phrases = extract_personas(parse_tree, word_list, quote_adjs,
							    itertools, stopwords, conjunctions,
							    bes, haves, wn, feels, print_lines)
		
		describers, all_phrases = extract_personas(parse_tree, word_list, adjs,
							    				   itertools, stopwords, conjunctions,
							    				   bes, haves, wn, feels, print_lines)
	else:
		describers, all_phrases = extract_personas(parse_tree, word_list, add(adjs, quote_adjs),
							    				   itertools, stopwords, conjunctions,
							    				   bes, haves, wn, feels, print_lines)
		opinion_describers = {}
	#opinion_describers = (extract_personas(parse_tree, word_list,
	 #					  quote_adjs, itertools, stopwords, conjunctions, 
	 #				      bes, haves, wn, feels, print_lines))
	#all_describers = merge_describers(describers, opinion_describers)
	
	#return (describers, {}, describers)

	return ((describers, opinion_describers), all_phrases)

def get_describers(parse_tree, word_list, character, adjs, quote_adjs,
					 itertools, stopwords, conjunctions, bes, haves, wn, feels, pov, 
					 split_by_chapters, print_lines, differentiated):
	if pov:
		descriptions = pov_processing(parse_tree, word_list, character, adjs, quote_adjs, 
							   	   	  itertools, stopwords, conjunctions, bes, haves, wn, feels, 
							   	   	  print_lines, differentiated)
	elif split_by_chapters:
		descriptions = chapter_processing(parse_tree, word_list, character, adjs, quote_adjs, 
								   	   	  itertools, stopwords, conjunctions, bes, haves, wn, feels, 
				 				  	  	  print_lines, differentiated)
		
	else:
		(descriptions, all_phrases) = normal_processing(parse_tree, word_list, character, adjs, quote_adjs, 
					   							      itertools, stopwords, conjunctions, bes, haves, wn, feels, 
				 	  	  						 	  print_lines, differentiated)

	
	return (descriptions, all_phrases)

def add_opinions(describers, char_opinion_facts, char_opinion_states,
				 char_val):
	char_opinion_facts[char_val] = describers[0]
	char_opinion_states[char_val] = describers[1]


def product(parse_tree, itertools, people, adjectives, i):
	return ((p, a) for (p,a) in 
			itertools.product(people, adjectives) if 
			p and a and p != a)

def parent_or_nearby_vbz(parse_tree, p, i):
	return (is_pos_equal(parent(parse_tree, p, i), "VBZ") or 
			find_nearby_vbs(parse_tree, p, i, ["VBZ"]))

def det_describer_and_adj_parent_of_p(parse_tree, p, a, i):
	def prev_word_det(parse_tree, tup, i):
		if prev_word_exists(parse_tree, tup, i):
			return is_dependency_equal(prev_word(parse_tree, tup, i), "det")
		
		return False

	return (is_parent(p, a) and prev_word_det(parse_tree, a, i))

def classify_sibling_relationship(parse_tree, p, a, i, facts, 
										states, feelings, wn, feels, conjunctions):
	if in_feelings_set(wn, feels, word(a)):
		return feelings
	elif not is_pos_of(parent(parse_tree, a, i), "VB"):
		if in_in_between_or_root_a(parse_tree, p, a, i, conjunctions):
			return states
		else:
			return facts
	elif sibling_states_conditions(parse_tree, p, a, i):
		return states

def classify_descendant_relationship(parse_tree, p, a, i, facts, 
								   states, feelings, wn, feels, 
								   conjunctions, bes, haves):
	if det_describer_and_adj_parent_of_p(parse_tree, p, a, i):
		return facts
	elif in_feelings_set(wn, feels, word(a)):
		return feelings
	elif (ancestor_states_conditions(parse_tree, p, a, i,
									 conjunctions, bes, haves)):
		return states
	else:
		return facts

def classify_g_nibling_or_descendant_relationship(parse_tree, a, p, i, facts, 
									states, feelings, wn, feels):
	if in_feelings_set(wn, feels, word(a)):
		return feelings
	elif is_pos_of(parent(parse_tree, p, i), "VB"):
		return states
	else:
		return facts

def sibling_relationship(parse_tree, p, a, i):
	return has_common_parent(p, a) and has_direct_dependency(parse_tree, a, i)

def descendant_relationship(parse_tree, p, a, i, conjunctions):
	return (
			is_ancestor(parse_tree, p, a, i) and 
		  	not nsubj_children(parse_tree, p, a, i, conjunctions) and 
		  	(
		   	 no_punct_in_between(parse_tree, p, a, p, i, conjunctions) or
		   	 not has_VB_in_path(parse_tree, p, a, i)
		  	)
		   )

def g_nibling_or_descendant_relationship(parse_tree, a, p, i, conjunctions):
	return (
			(
			 is_g_nibling(parse_tree, a, p, i) or 
			 is_ancestor(parse_tree, a, p, i)
			) and 
	 		has_direct_dependency(parse_tree, a, i) and 
		  	 (
		  	  not is_dependency_of(parent(parse_tree, a, i), "dobj") or 
		  	  is_g_nibling(parse_tree, a, p, i)
		  	 ) and
		  	not nsubj_children(parse_tree, p, a, i, conjunctions)
		   )

def nearby_words_conditions(parse_tree, p, i, conjunctions, bes, haves):
	return (
			parent_or_nearby_vbz(parse_tree, p, i) or 
			next_word_had_or_is_conditions(parse_tree, p, i, bes, haves) or 
			have_condition(parse_tree, p, i, conjunctions)
		   )

def persona_facet(parse_tree, p, a, i, facts, states, feelings, invalid, wn, 
				  feels, conjunctions, bes, haves):
	facet = {}

	if nearby_words_conditions(parse_tree, p, i, conjunctions, bes, haves):
		facet = facts
	
	if sibling_relationship(parse_tree, p, a, i):
		if not facet:
			facet = classify_sibling_relationship(parse_tree, p, a, 
													    i, facts, states, 
													    feelings, wn, 
													    feels, 
													    conjunctions)
	elif descendant_relationship(parse_tree, p, a, i, conjunctions):
		if not facet:
			facet = classify_descendant_relationship(parse_tree, p, a, i, 
												   	      facts, states, 
												   		  feelings, wn, feels, 
												   		  conjunctions, bes, haves)
	elif g_nibling_or_descendant_relationship(parse_tree, a, p, i, conjunctions):
		if not facet:
			facet = classify_g_nibling_or_descendant_relationship(parse_tree, a, p, i, 
					 							    facts, states, 
					 							    feelings, wn, feels)
	else:
		facet = invalid
	
	return facet

def conj_children(parse_tree, p, i, people):
	return [tup for tup in people if 
			is_parent(tup, p) and 
			is_dependency_of(tup, "conj") and 
			not nsubj_tups_of_char_id(parse_tree[i][index(tup):], char_id(p))]

def map_person_to_phrase(word_list, p, a, i, description, dictionary, 
						 facts, states, feelings, invalid, all_phrases, 
						 print_these):
	print_these.append((p, a, i, 0))
	add_to_set(word_list, p, a, i, char_id(p), description, dictionary, facts,
			   states, feelings, invalid, all_phrases)

def find_personas(parse_tree, word_list, i, facts, states, feelings, invalid, all_phrases,
				  itertools, stopwords, conjunctions, bes, haves, wn, feels, print_these):
	
	people = get_nsubj_people(parse_tree, i)	
	adjectives = get_adjectives(parse_tree, i)

	for p, a in product(parse_tree, itertools, people, adjectives, i):
		dictionary = persona_facet(parse_tree, p, a, i, facts, 
								   states, feelings, invalid, wn, feels, 
								   conjunctions, bes, haves)

		if dictionary in (facts, states, feelings, invalid):
			description = get_description(parse_tree, people, p, a, i, stopwords, 
									   	  conjunctions, bes, haves)
			
			conj_people = conj_children(parse_tree, p, i, 
						 			    get_people(parse_tree, i))
						 	
			for person in conj_people:
				description = bigger(description, get_description(parse_tree, people, person, 
												 				  a, i, stopwords, 
												 				  conjunctions, bes, haves))

			for person in [p] + conj_people:
				map_person_to_phrase(word_list, person, a, i, description, 
									 dictionary, facts, states, feelings, 
									 invalid, all_phrases, print_these)

			
def extract_personas(parse_tree, word_list, adjs, itertools, stopwords,
						 conjunctions, bes, haves, wn, feels, print_lines):
	print_these = []
	facts = {}
	states = {}
	feelings = {}
	invalid = {}
	all_phrases = set()
	
	for i in sorted(adjs):
		find_personas(parse_tree, word_list, i, facts, states, feelings, invalid, 
		 			  all_phrases, itertools, stopwords, conjunctions,
		 			  bes, haves, wn, feels, print_these)
	
	if print_lines:
		print_sentence_data(parse_tree, word_list, print_these)
	

	return ((facts, states, feelings, invalid), all_phrases)

def init_adjs(parse_tree, sentence_token):
	adjs = {}

	for i in range(max(sentence_token)):
		if has_JJ_and_nsubj(parse_tree[i], i):
			adjs[i] = parse_tree[i]

	return adjs

def init_parse_tree(sentence_token, norm_tok_list, norm_htok_list, pos_list,
					 dep_list, ch_id_list, word_list, norm_word_list):
	parse_tree = {}
	
	for i in range(max(sentence_token)):
		parse_tree[i] = zip(norm_tok_list[i], norm_htok_list[i], pos_list[i],
							dep_list[i], ch_id_list[i], word_list[i],
		  					norm_word_list[i])

	return parse_tree

def write_pickle(pickle, variable, parse_tree, describers, quote_set, adjs, quote_adjs,
				 opinion_describers, all_describers):
	
	variable['describers'] = describers
	variable['facts'] = describers[0]
	variable['states'] = describers[1]
	variable['parse_tree'] = parse_tree
	variable['quote_set'] = quote_set
	variable['adjs'] = adjs
	variable['quote_adjs'] = quote_adjs
	variable['opinion_describers'] = describers
	#variable['opinion_facts'] = opinion_describers[0]
	#variable['opinion_states'] = opinion_describers[1]
	variable['all_describers'] = all_describers
	
	with open('variable.pkl', 'wb') as fp:
		pickle.dump(variable, fp, pickle.HIGHEST_PROTOCOL)