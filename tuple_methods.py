def index(tup):
	return tup[0]

def parent_index(tup):
	return tup[1]

def pos(tup):
	return tup[2]

def dep(tup):
	return tup[3]

def char_id(tup):
	return tup[4]

def word(tup):
	return tup[5]

def norm_word(tup):
	return tup[6]

def is_root(tup):
	return parent_index(tup) == -1

def is_person(tup):
	return char_id(tup) != -1

def is_adjective(tup):
	return is_pos_of(tup, "JJ")

def is_adverb(tup):
	return is_pos_of(tup, "RB")	
	
def is_parent(tup1, tup2):
	return parent_index(tup1) == index(tup2)
	
def has_common_parent(tup1, tup2):
	return parent_index(tup1) == parent_index(tup2) and tup1 != tup2 

def is_dependency_of(tup, string):
	return dep(tup).startswith(string)

def is_dependency_of_any(tup, strings):
	return any(is_dependency_of(tup, string) for string in strings)

def is_dependency_equal(tup, string):
	return dep(tup) == string

def is_dependency_equal_any(tup, strings):
	return any(is_dependency_equal(tup, string) for string in strings)

def is_pos_of(tup, string):
	return pos(tup).startswith(string)

def is_pos_of_any(tup, strings):
	return any(is_pos_of(tup, string) for string in strings)

def is_pos_equal(tup, string):
	return pos(tup) == string

def is_pos_equal_any(tup, strings):
	return any(is_pos_equal(tup, string) for string in strings)

def is_word_equal(tup, string):
	return word(tup) == string

def is_word_equal_any(tup, strings):
	return any(is_word_equal(tup, string) for string in strings)

def is_lower_word_equal(tup, string):
	return word(tup).lower() == string

def is_lower_word_equal_any(tup, strings):
	return any(is_lower_word_equal(tup, string) for string in strings)

def is_norm_word_equal(tup, string):
	return norm_word(tup) == string

def is_norm_word_equal_any(tup, string):
	return any(is_norm_word_equal(tup, string) for string in strings)

def is_norm_word_of(tup, string):
	return norm_word(tup).startswith(string)

def is_norm_word_of_any(tup, strings):
	return any(is_norm_word_of(tup, string) for string in strings)

def is_same_norm_word(tup1, tup2):
	return norm_word(tup1) == norm_word(tup2)

def have_same_dependency(tup1, tup2):
	return dep(tup1) == dep(tup2)

def is_a_be(tup):
	bes = ["'s", "is", "was", "were", "be", "would", "'ll", "will"]
	haves = ["'d", "had", "have", "has"]
	
	return is_norm_word_of_any(tup, (bes+haves))

def is_child_in(tup, li):
	return [parent for parent in li if is_parent(tup, parent)]

def has_JJ_and_nsubj(li, i):
	return (any(tup for tup in li if is_pos_of(tup, "JJ")) and 
			any(tup for tup in li if is_dependency_of(tup, "nsubj")))

def nsubj_tups_of_char_id(li, ch_id):
	return [tup for tup in li if 
			is_dependency_of(tup, "nsubj") and 
			char_id(tup) == ch_id]

def previous_item_exists(li, tup):
	return li.index(tup) - 1 >= 0

def previous_item(li, tup):
	return li[li.index(tup) - 1]

def prev_person_is_same(people, tup):
	if previous_item_exists(people, tup):
		prev = previous_item(people, tup)
		if prev in people:
			return char_id(tup) == char_id(prev)

	return False

def not_first_person(tup, people):
	if tup in people:
		return (people.index(tup) != 0 and 
				not prev_person_is_same(people, tup))
	else:
		return False
