from tuple_methods import *
from wordnet_methods import *
from string_methods import *
from print_methods import *

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

def prev_word_det(parse_tree, tup, i):
	if near_word_exists(parse_tree, tup, i, -1):
		return is_dependency_equal(near_word(parse_tree, tup, i, -1), "det")
	
	return False

def is_g_nibling(parse_tree, tup1, tup2, i):
	return (is_ancestor(parse_tree, tup2, parent(parse_tree, tup1, i), i))


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

def child_negs(parse_tree, li, i):
	return ([tup for tup in parse_tree[i] if 
			is_dependency_equal(tup, "neg") and
	 		any(is_parent(tup, x) for x in li) and
	 		tup not in li])

def between_negs(parse_tree, p, a, i):
	return ([tup for tup in parse_tree[i] if 
			 is_dependency_of(tup, "neg") and 
			 index(p) < index(tup) and 
			 index(tup) < index(a)])

def prev_negs(parse_tree, li, p, a, i, people, conjunctions):
	return ([tup for tup in parse_tree[i] if 
			is_dependency_equal(tup, "neg")
	 		and parse_tree[i].index(tup) < parse_tree[i].index(a)
	  		and no_conj_in_between(parse_tree, tup, a, i, conjunctions) and
	  		no_punct_in_between(parse_tree, tup, a, i, conjunctions) and
	  		tup not in li if 
	  		not not_first_person(p, people)])

def all_negs(parse_tree, adj_list, p, a, i, people, conjunctions):
	return (child_negs(parse_tree, adj_list, i) +
			between_negs(parse_tree, p, a, i) +
			prev_negs(parse_tree, adj_list, p, a, i, people, conjunctions))

def is_near_word_JJ_or_RB(parse_tree, tup, i, k):
	if near_word_exists(parse_tree, tup, i, k):
		return is_pos_of_any(near_word(parse_tree, tup, i, k), ["JJ", "RB"])
	else:
		return False

def surrounding_words_linked(parse_tree, tup, i, conjunctions):
	return ((is_near_word_JJ_or_RB(parse_tree, tup, i, -1) and
			 is_near_word_JJ_or_RB(parse_tree, tup, i, 1)) or 
			 (have_same_dependency(near_word(parse_tree, tup, i, -1),
								  near_word(parse_tree, tup, i, 1))
			 ) or
			 ((is_dependency_of_any(near_word(parse_tree, tup, i, 1), ["amod", "conj", "advcl"]) or
			   (is_word_equal_any(near_word(parse_tree, tup, i, 1), 
			   							   conjunctions) and 
			    is_near_word_JJ_or_RB(parse_tree, tup, i, 2))) and
			  is_word_equal(tup, ","))
		   )

def remove_adj_splitters(parse_tree, li, i, conjunctions):
	return [tup for tup in li if 
			not surrounding_words_linked(parse_tree, tup, i, conjunctions)]

def get_conjunctions(parse_tree, li, i, conjunctions):
	#assumes list is sorted
	indices = range(li[0][0], li[-1][0])
	return ([tup for tup in parse_tree[i] if 
			word(tup) in conjunctions
	 		and index(tup) in indices])

def is_there_one_as(parse_tree, li, i):
	as_words = [tup for tup in li if is_word_equal(tup, "as")]
	if len(as_words) == 1:
		return parse_tree[i].index(as_words[0])
	else:
		return -1

def check_for_as(parse_tree, li, i):
	first_as = is_there_one_as(parse_tree, li, i)
	if first_as != -1:
		second_as = is_there_one_as(parse_tree, parse_tree[i][first_as+1:], i)
		if second_as != -1:
			second_as_tup = parse_tree[i][second_as]
			return [second_as_tup, parent(parse_tree, second_as_tup,i)]
	
	return []


def get_punctuations(parse_tree, li, i):
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
	return not is_dependency_of_any(a, ["det", "advcl", "case", "acl:relcl"])


def check_amod_advmod_conds(parse_tree, a, i):
	return (is_dependency_equal_any(a, ["amod", "advmod"]) and 
			not is_dependency_of(parent(parse_tree, a, i), "nsubj"))

def is_prev_word_a_be(parse_tree, tup, i):
	if near_word_exists(parse_tree, tup, i, -1):
		return is_a_be(near_word(parse_tree, tup, i, -1))
	else:
		return False

def get_advmods(parse_tree, a, i):
	return ([tup for tup in parse_tree[i] if
			is_dependency_equal_any(tup, ["advmod", "det"]) and 
			(has_common_parent(tup, a) or 
			is_parent(tup, a)) and 
			tup != a and
			is_prev_word_a_be(parse_tree, tup, i)]) 

def get_nmod_children(parse_tree, a, i):
	return ([tup for tup in parse_tree[i] if 
			is_dependency_of(tup, "nmod:") and 
			(is_parent(tup, a) or
			has_common_parent(tup, a) or 
			tup == a or 
			tup == parent(parse_tree, a, i))])

def get_conj_children(parse_tree, a, i):
	return ([tup for tup in parse_tree[i] if 
			is_dependency_of(tup, "conj:") and 
			not (is_pos_equal(tup, "VBD") or 
			is_pos_equal(tup, "VB")) and
			(is_parent(tup, a) or 
			has_common_parent(tup, a) or
			tup == a or 
			tup == parent(parse_tree, a, i))])


def find_RBs(parse_tree, a, i):
	return	([tup for tup in parse_tree[i] if 
			 is_adverb(tup) and
			 is_parent(tup, a)])

def find_valid_adj_parents(parse_tree, a, i, conjunctions):
	parent_tup = parent(parse_tree, a, i)

	if (add_parent_of_adj_conds(parse_tree, a, i) and 
		no_punct_in_between(parse_tree, a, parent_tup, i, conjunctions) and 
		no_conj_in_between(parse_tree, a, parent_tup, i, conjunctions)):
		return [parent_tup]
	else:
		return []

def add_trait_preps(parse_tree, a, i):
	return ([tup for tup in parse_tree[i] if 
			is_pos_equal(tup, "IN") and
	 		not is_dependency_equal(tup, "mark") and 
	 		is_parent(tup, a)])

def get_trait_advmods(parse_tree, a, i):
	return ([tup for tup in parse_tree[i] if 
			is_dependency_equal(tup, "advmod") and 
			is_parent(tup, a) and 
			tup != a])

def get_adj_advcls(parse_tree, a, i):
	return ([tup for tup in parse_tree[i] if 
			is_dependency_equal(tup, "advcl") and 
			is_adjective(tup) and 
			(is_parent(tup, a) or
			has_common_parent(tup, a)) and 
			tup != a])

def get_adj_acl_relcls(parse_tree, p, i):
	return ([tup for tup in parse_tree[i] if 
			is_dependency_equal(tup, "acl:relcl") and 
			is_adjective(tup) and 
			(is_parent(tup, p) or
			has_common_parent(tup, p)) and 
			tup != p])

def get_in_words(parse_tree, p, a, i):
	return ([tup for tup in parse_tree[i] if 
			is_word_equal(tup, "in") and 
			parse_tree[i].index(tup) < parse_tree[i].index(a) and 
			parse_tree[i].index(p) < parse_tree[i].index(tup)])
	
def check_for_in(parse_tree, p, a, i, conjunctions):
	in_words = get_in_words(parse_tree, p, a, i)
	if in_words:
		word = sorted(in_words)[-1]
		return (no_conj_in_between(parse_tree, word,
								   a, i, conjunctions) and 
				no_punct_in_between(parse_tree, word, a, i, conjunctions))
	else:
		return False

def no_punct_in_between(parse_tree, tup1, tup2, i, conjunctions):
	return not (remove_adj_splitters(parse_tree, 
									 get_punctuations(
									 				  parse_tree, 
									 				  all_words_in_between
									 				  	(
									 				  	 parse_tree, 
									 				  	 sorted([tup1, tup2]), 
									 				  	 i
									 				  	), 
									 				  i
									 				 ), 
									 i,
									 conjunctions
									)
			   )

def no_conj_in_between(parse_tree, tup1, tup2, i, conjunctions):
	return not (remove_adj_splitters(parse_tree,
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
									 i,
									 conjunctions
									 ) 
				)
	
def form_of_be(parse_tree, a, i):
	return ([tup for tup in parse_tree[i] if 
			is_a_be(tup) and
			is_parent(tup, a)])

def near_word_exists(parse_tree, tup, i, k):
	return (index(tup) + k >= 0 and index(tup) + k < len(parse_tree[i]))

def near_word(parse_tree, tup, i, k):
	return parse_tree[i][index(tup) + k]

def get_nearby_vbs(parse_tree, tup, i, vb_strings):
	vibs = []
	
	if near_word_exists(parse_tree, tup, i, -1):
		prev = near_word(parse_tree, tup, i, -1)
		if (is_pos_equal_any(prev, vb_strings)):
			vibs.append(prev)
	if near_word_exists(parse_tree, tup, i, 1):
		next = near_word(parse_tree, tup, i, 1)
		if (is_pos_equal_any(next, vb_strings)):
			vibs.append(next)
	
	return vibs

def add_parent_of_adj_conds(parse_tree, a, i):
	return (is_dependency_of_any(a, 
								["nmod:", "conj:", "xcomp", "dobj", "amod"]
								) or
	 		check_amod_advmod_conds(parse_tree, a, i)
	 		)

def parent_sibling_negs(parse_tree, a, i):
	return ([tup for tup in parse_tree[i] if 
			is_dependency_equal(tup, "neg") and
			(is_parent(tup, a) or
			has_common_parent(tup, a))])

def find_negs(parse_tree, a, i):
	return sorted(add_nt_words(parse_tree, 
							   add_prevs(parse_tree, 
										 parent_sibling_negs(parse_tree,
										 					 a,
										 					 i),
										 i),
							   i))

def words_between_adj_and_parent(parse_tree, a, i):
	indices = (range(min(index(a), parent_index(a)),
				max(index(a), parent_index(a)) + 1))
	
	tups = [tup for tup in parse_tree[i] if index(tup) in indices]
	
	return sorted(tups)

def punct_split(parse_tree, li, p, a, i, conjunctions):
	bigl = []
	phrase = []
	last = 0
	
	for word in li:
		if (is_dependency_equal(word, "punct") and 
			not surrounding_words_linked(parse_tree, word, i, conjunctions)):
			bigl.append(li[last:li.index(word)])
			last = li.index(word) + 1
	bigl.append(li[last:])


	for sublist in bigl:
		if (a in sublist or 
			is_next_(parse_tree, p, i, sublist, 0) or 
			is_first_word_person(sublist, p)):
			phrase += sublist
	
	return phrase

def is_first_word_person(li, p):
	if li :
		return char_id(li[0]) == char_id(p)
	else:
		return False

def is_next_(parse_tree, p, i, sublist, k):
	if sublist and p and near_word_exists(parse_tree, p, i, 1):
		return near_word(parse_tree, p, i, 1) == sublist[k]
	else:
		return False

def sibling_states_conditions(parse_tree, p, a, i):
	return ((not (is_dependency_of(a, "dep")) and
			 not (is_dependency_of(a, "nmod") and
			 	  not is_adjective(parent(parse_tree, a, i))
			 	 )
			 ) and
			not ([tup for tup in parse_tree[i]
	  			 if is_dependency_of(tup, "nsubj")
	  			 and is_parent(tup, a)]) and
	  		not ([tup for tup in parse_tree[i]
	  			 if is_dependency_of(tup, "dobj") and 
	  			 is_pos_of(tup, "PRP") and 
	 			 has_common_parent(tup, a) and 
	 			 tup != p]))

def check_conj_and_nmod(parse_tree, a, i):
	nmod_list = []
	conj_list = []

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

def add_preps_and_coord_conjs(parse_tree, adj_list, p, a, i):
	return ins(parse_tree, p, a, i) + ccs(parse_tree, adj_list, p, a, i)

def is_related(tup1, tup2):
	return has_common_parent(tup1, tup2) or is_parent(tup1, tup2)

def nsubj_children(parse_tree, p, a, i):
	return (
			[
			 tup for tup in parse_tree[i] if 
			 is_dependency_of(tup, "nsubj") and 
			 (is_parent(tup, a) or 
			  (
			   is_pos_of(parent(parse_tree, a, i), "VB") and 
			   is_related(tup, parent(parse_tree, a, i))
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

def add_all_dep_children(parse_tree, strings, li, filled_li, i):
	return ([tup for tup in parse_tree[i] if 
			is_dependency_of_any(tup, strings) and
			is_child_in(tup, filled_li) and 
			tup not in li])

def add_all_pos_children(parse_tree, strings, li, filled_li, i):
	return ([tup for tup in parse_tree[i] if 
			is_pos_of_any(tup, strings) and
			is_child_in(tup, filled_li) and
			tup not in li])

def get_the_dep_children(parse_tree, strings, li, filled_li, i, deps):
	
	if li:
		child_deps = add_all_dep_children(parse_tree, strings, li, filled_li, i)
		deps += child_deps
		return get_the_dep_children(parse_tree, 
									strings, 
									child_deps, 
									child_deps,
									i, 
									deps)

	return deps

def get_the_pos_children(parse_tree, strings, li, filled_li, i, pos):
	if li:
		child_pos = add_all_pos_children(parse_tree, strings, li, filled_li, i)
		pos += child_pos
		return get_the_pos_children(parse_tree, 
									strings, 
									child_pos, 
									child_pos,
									i, 
									pos)
	
	return pos

def recursively_add_all_dep_children(parse_tree, strings, li, filled_li, i):
	return get_the_dep_children(parse_tree, strings, li, filled_li, i, deps = [])

def recursively_add_all_pos_children(parse_tree, strings, li, filled_li, i):
	return get_the_pos_children(parse_tree, strings, li, filled_li, i, pos = [])

	
def recursively_add_all_dep_and_pos_children(parse_tree, dep_strings, 
											 pos_strings, adj_list, i):

	descendants = ["do while loop emulator"]
	while descendants:
		descendants = []
		descendants += (recursively_add_all_pos_children
							(
						 	 parse_tree, 
						 	 pos_strings, 
						 	 adj_list,
						 	 all_words_in_between(parse_tree,
						 						  filter_duplicates(adj_list),
						 						  i),
						 	 i
							))

		descendants += (recursively_add_all_dep_children
							(
							 parse_tree,
							 dep_strings,
							 adj_list,
							 all_words_in_between(parse_tree,
							 					  filter_duplicates(adj_list),
							 					  i),
							 i
							))

		adj_list += descendants
		
	return adj_list

def ancestor_states_conditions(parse_tree, p, a, i, conjunctions):
	return (not form_of_be(parse_tree, a, i) or
			get_nearby_vbs(parse_tree, a, i, ["VBG", "VBD"]) or
			check_for_in(parse_tree, p, a, i, conjunctions))

def add_nt_words(parse_tree, negs, i):
	for neg in negs:
		if is_word_equal(neg, "n't"):
			negs.append(near_word(parse_tree, neg, i, -1))
	return negs

def add_prevs(parse_tree, negs, i):
	prevs = []
	for neg in negs:
		if near_word_exists(parse_tree, neg, i, -1):
			prev = near_word(parse_tree, neg, i, -1)
			if (has_common_parent(prev, neg) and 
				not is_dependency_equal(prev, "punct")):
				prevs.append(prev)
	
	return negs + prevs

def add_to_set(char_id, adj_list, container, i):
	if char_id not in container:
		container[char_id] = {}
	
	if i not in container[char_id]:
		container[char_id][i] = []
		container[char_id][i].append(adj_list)
	else:
		added = False
		for j in range(len(container[char_id][i])):
			if (is_subset(container[char_id][i][j], adj_list) or
				is_subset(adj_list, container[char_id][i][j])):
				container[char_id][i][j] =\
				superset(container[char_id][i][j], adj_list)
				added = True
		if not added:
			container[char_id][i].append(adj_list)


def check_for_xcomp(parse_tree, adj_list, a, i):
	if is_dependency_of(a, "xcomp"):
		adj_list = words_between_adj_and_parent(parse_tree, a, i)
	
	return adj_list

def add_dependents(parse_tree, adj_list, p, a, i, conjunctions):
	
	adj_list = check_for_xcomp(parse_tree, adj_list, a, i)
	
	adj_list += find_negs(parse_tree, a, i)
	adj_list += find_RBs(parse_tree, a, i)
	
	adj_list += get_nearby_vbs(parse_tree, a, i, ["VBG", "VBD", "VBZ"])
	adj_list += get_nearby_vbs(parse_tree, p, i, ["VBG", "VBD", "VBZ"])
	
	adj_list += get_adj_advcls(parse_tree, a, i)
	adj_list += get_adj_acl_relcls(parse_tree, p , i)
	
	adj_list += add_trait_preps(parse_tree, a, i)
	adj_list += get_advmods(parse_tree, a, i)
	adj_list += check_conj_and_nmod(parse_tree, a, i)
	
	adj_list += find_valid_person_parents(parse_tree, p, i, conjunctions)	
	adj_list += find_valid_adj_parents(parse_tree, a, i, conjunctions)

	adj_list += add_preps_and_coord_conjs(parse_tree, adj_list, p, a, i)
	adj_list += get_punctuations(parse_tree, adj_list, i)
	adj_list += check_for_as(parse_tree, filter_duplicates(adj_list), i)

	return adj_list
	
def refine(parse_tree, adj_list, people, p, a, i, stopwords, conjunctions):
	
	adj_list += all_negs(parse_tree, adj_list, p, a, i, people, conjunctions)
	adj_list = recursively_add_all_dep_and_pos_children(parse_tree, 
														 ["xcomp", "ccomp", 
														  "nmod", "conj", 
														  "dobj", "cc", "aux"],
														 ["VB", "RB", "WRB"],
														 adj_list,
														 i)
		
	adj_list = all_words_in_between(parse_tree, filter_duplicates(adj_list), i)
	
	adj_list = punct_split(parse_tree, all_words_in_between(parse_tree, 
															adj_list, 
															i), 
						   p, a, i, conjunctions)

	adj_list = all_words_in_between(parse_tree, filter_duplicates(adj_list), i)	
	adj_list = remove_stop_words(adj_list, stopwords)

	return filter_duplicates(adj_list)

def add_parent_of_person_conds(parse_tree, p, i):
	return (is_pos_of(parent(parse_tree, p, i), "VB"))

def find_valid_person_parents(parse_tree, p, i, conjunctions):
	parent_tup = parent(parse_tree, p, i)

	if (add_parent_of_person_conds(parse_tree, p, i) and 
		no_punct_in_between(parse_tree, p, parent_tup, i, conjunctions)):
		return [parent_tup]
	else:
		return []

def description(parse_tree, people, p, a, i, stopwords, conjunctions):
	adj_list = add_dependents(parse_tree, [a], p, a, i, conjunctions)		
	adj_list = refine(parse_tree, filter_duplicates(adj_list), people, p, a, i, 
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

def print_stuff(parse_tree, word_list, (p, a, i, facts)):
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

def print_all_chars_character_wise(describers, character):
	facts = describers[0]
	states = describers[1]
	feelings = describers[2]

	for id in sorted(character):
		if id in facts or id in feelings or id in states:
			print'____________________________________________________________'
			print id, sorted(character[id])
			print '----------------'
			print 'FACTS'
			print '----------------'
			if id in facts:
				for val in facts[id]:
					print val, get_adj_from_list(facts[id][val])
			print '----------------'
			print 'STATES'		
			print '----------------'
			if id in states:
				for val in states[id]:
					print val, get_adj_from_list(states[id][val])
			print '----------------'
			print 'FEELINGS'		
			print '----------------'
			if id in feelings:
				for val in feelings[id]:
					print val, get_adj_from_list(feelings[id][val])
			
			print'____________________________________________________________'

def print_all_chars(describers, character):
	
	facts = describers[0]
	states = describers[1]
	feelings = describers[2]

	print'____________________________________________________________'
	print 'FACTS'
	print'____________________________________________________________'

	for id in facts:
		print id, sorted(character[id]), '---'
		for val in facts[id]:
			print val, get_adj_from_list(facts[id][val])
		print '------------------------------------'
	print len(facts)

	print'____________________________________________________________'
	print 'STATES'
	print'____________________________________________________________'

	for id in states:
		print id, sorted(character[id]), '---'
		for val in states[id]:
			print val, get_adj_from_list(states[id][val])
		print '------------------------------------'
	print len(states)

	print'____________________________________________________________'
	print 'FEELINGS'
	print'____________________________________________________________'

	for id in feelings:
		print id, sorted(character[id]), '---'
		for val in feelings[id]:
			print val, get_adj_from_list(feelings[id][val])
		print '------------------------------------'
	print len(feelings)

	print'____________________________________________________________'

def print_all(parse_tree, word_list, print_these):
	for tup in print_these:
		print_stuff(parse_tree, word_list, tup)

def get_adj_from_list(adj_list):
	stringed_adjs = []
	adjective = ""
	for li in adj_list:
		adjective = ""
		for item in li:
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
		stringed_adjs.append(adjective)

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

def merge_describers(d1, d2):
	d3 = ({},{}, {})
	for i in range(3):
		for charId in d1[i]:
			for val in d1[i][charId]:
				for adj_list in d1[i][charId][val]:
					add_to_set(charId, adj_list, d3[i], val)

		for charId in d2[i]:
			for val in d2[i][charId]:
				for adj_list in d2[i][charId][val]:
					add_to_set(charId, adj_list, d3[i], val)

	return d3

def get_describers(parse_tree, word_list, character, adjs, quote_adjs,
					 itertools, stopwords, conjunctions, wn, feels, pov, 
					 split_by_chapters, print_lines):
	if pov:
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
			describers = find_the_adjectives(parse_tree, word_list,
											 pov_adjs[person_id], itertools,
											 stopwords, conjunctions, wn,
											 feels, print_lines)
			pov_quote_adjs = get_id_quotes(quote_set, quote_adjs, person_id)
			opinion_describers = find_the_adjectives(parse_tree,
													 word_list,
													 pov_quote_adjs, 
													 itertools,
													 stopwords,
													 conjunctions, wn,
													 feels, print_lines)
			all_describers = merge_describers(describers, opinion_describers)
			#print_all_chars(all_describers, character)
			print_all_chars_character_wise(all_describers, character)

	elif split_by_chapters:
		chapter_adjs = chapter_split(adjs, chapter_indices)
		chapter_quote_adjs = chapter_split(quote_adjs, chapter_indices)
		

		for chap in range(len(chapter_indices)):
			print_chapters_stuff(chap, chapter_names, chapter_indices,
								 chapter_quote_adjs)
			describers = find_the_adjectives(parse_tree, word_list, 
											 chapter_adjs[chap],
			 								 itertools, stopwords,
			 								 conjunctions, wn, feels,
			 								 print_lines)
			opinion_describers = find_the_adjectives(parse_tree, word_list, 
													 chapter_quote_adjs[chap],
													 itertools, stopwords,
													 conjunctions, wn,
													 feels, print_lines)
			all_describers = merge_describers(describers, opinion_describers)
			#print_all_chars(all_describers, character)
			print_all_chars_character_wise(all_describers, character)
		
	else:
		describers = find_the_adjectives(parse_tree, word_list, adjs,
										 itertools, stopwords, conjunctions,
										 wn, feels, print_lines)
		opinion_describers = (find_the_adjectives(parse_tree, word_list,
		 					  quote_adjs, itertools, stopwords, conjunctions, 
		 				      wn, feels, print_lines))
		all_describers = merge_describers(describers, opinion_describers)
		#print_all_chars(all_describers, character)
		print_all_chars_character_wise(all_describers, character)

	return (describers, opinion_describers, all_describers)

def add_opinions(describers, char_opinion_facts, char_opinion_states,
				 char_val):
	char_opinion_facts[char_val] = describers[0]
	char_opinion_states[char_val] = describers[1]
	
def get_description(parse_tree, people, p, a, i, conj_p_children, dictionary, stopwords, 
				 conjunctions, print_these):
	adj_list = description(parse_tree, people, p, a, i, stopwords, 
							conjunctions)

	for child in conj_p_children:
		adj_list = bigger(adj_list, description(parse_tree, people, child, 
												 a, i, stopwords, 
												 conjunctions))
		
	for person in [p] + conj_p_children:
		print_these.append((person, a, i, 0))
		add_to_set(char_id(person), adj_list, dictionary, i)

def conj_p_children(parse_tree, p, i, people):
	return [tup for tup in people if 
			is_parent(tup, p) and 
			is_dependency_of(tup, "conj") and 
			not nsubj_tups_of_char_id(parse_tree[i][index(tup):], char_id(p))]

def product(parse_tree, itertools, people, adjectives, i):
	return ((p, a) for (p,a) in 
			itertools.product(people, adjectives) if 
			p and a and p != a)

def trait_verb_conds(parse_tree, p, i):
	return (is_pos_equal(parent(parse_tree, p, i), "VBZ") or 
			get_nearby_vbs(parse_tree, p, i, ["VBZ"]))

def trait_det_conds(parse_tree, p, a, i):
	return (is_parent(p, a) and prev_word_det(parse_tree, a, i))

def classify_common_parent_relationship(parse_tree, p, a, i, facts, 
										states, feelings, wn, feels, conjunctions):
	if trait_verb_conds(parse_tree, p, i):
		return facts
	elif in_sense_set(wn, feels, word(a)):
		return feelings
	elif not is_pos_of(parent(parse_tree, a, i), "VB"):
		if (check_for_in(parse_tree, p, a, i, conjunctions) or 
			is_root(a)):
			return states
		else:
			return facts
	elif sibling_states_conditions(parse_tree, p, a, i):
		return states

def classify_ancestor_relationship(parse_tree, p, a, i, facts, 
								   states, feelings, wn, feels, 
								   conjunctions):
	if (trait_verb_conds(parse_tree, p, i) or
		trait_det_conds(parse_tree, p, a, i)):
		return facts
	elif in_sense_set(wn, feels, word(a)):
			return feelings
	elif (ancestor_states_conditions(parse_tree, p, a, i,
									 conjunctions) or 
		  is_root(a)):
		return states
	else:
		return facts

def classify_g_nibling_relationship(parse_tree, p, a, i, facts, 
									states, feelings, wn, feels):
	if trait_verb_conds(parse_tree, p, i):	
		return facts
	elif in_sense_set(wn, feels, word(a)):
		return feelings
	elif is_pos_of(parent(parse_tree, p, i), "VB"):
		return states
	else:
		return facts

def parent_relationship(parse_tree, p, a, i):
	return has_common_parent(p, a) and has_direct_dependency(parse_tree, a, i)

def ancestor_relationship(parse_tree, p, a, i, conjunctions):
	return (
			is_ancestor(parse_tree, p, a, i) and 
		  	not nsubj_children(parse_tree, p, a, i) and 
		  	(
		   	 no_punct_in_between(parse_tree, p, a, i, conjunctions) or
		   	 not has_VB_in_path(parse_tree, p, a, i)
		  	)
		   )

def g_nibling_relationship(parse_tree, p, a, i):
	return (
			is_g_nibling(parse_tree, p, a, i) and 
	 		not is_root(parent(parse_tree, p, i)) and 
		  	has_direct_dependency(parse_tree, a, i) and 
		  	not nsubj_children(parse_tree, p, a, i)
		   )

def persona_facet(parse_tree, p, a, i, facts, states, feelings, wn, 
				  feels, conjunctions):
	if parent_relationship(parse_tree, p, a, i):
		return classify_common_parent_relationship(parse_tree, p, a, 
												   i, facts, states, 
												   feelings, wn, 
												   feels, 
												   conjunctions)
	elif ancestor_relationship(parse_tree, p, a, i, conjunctions):
		return classify_ancestor_relationship(parse_tree, p, a, i, 
											  facts, states, 
											  feelings, wn, feels, 
											  conjunctions)
	elif g_nibling_relationship(parse_tree, p, a, i):
		return classify_g_nibling_relationship(parse_tree, p, a, i, 
											   facts, states, 
											   feelings, wn, feels)
	else:
		return {}

def map_adjectives(parse_tree, word_list, i, facts, states, feelings, 
				   itertools, stopwords, conjunctions, wn, feels, print_these,
				   adj_set_ids):
	
	people = get_nsubj_people(parse_tree, i)	
	adjectives = get_adjectives(parse_tree, i)

	for p, a in product(parse_tree, itertools, people, adjectives, i):
		dictionary = persona_facet(parse_tree, p, a, i, facts, 
								   states, feelings, wn, feels, 
								   conjunctions)

		if (id(dictionary) in adj_set_ids):
			get_description(parse_tree, 
						 people, 
						 p, a, i, 
						 conj_p_children(parse_tree, p, i, 
						 				 get_people(parse_tree, i)), 
						 dictionary, 
						 stopwords, 
						 conjunctions, 
						 print_these)
		
def find_the_adjectives(parse_tree, word_list, adjs, itertools, stopwords,
						 conjunctions, wn, feels, print_lines):
	print_these = []
	facts = {}
	states = {}
	feelings = {}
	
	for i in sorted(adjs):
		map_adjectives(parse_tree, word_list, i, facts, states, feelings,
		 			   itertools, stopwords, conjunctions, wn, feels, 
	 				   print_these, adj_set_ids = [id(facts), id(states),
	 				   							   id(feelings)])
	
	if print_lines:
		print_all(parse_tree, word_list, print_these)
	
	return (facts, states, feelings)

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
	variable['opinion_facts'] = opinion_describers[0]
	variable['opinion_states'] = opinion_describers[1]
	variable['all_describers'] = all_describers
	
	with open('variable.pkl', 'wb') as fp:
		pickle.dump(variable, fp, pickle.HIGHEST_PROTOCOL)