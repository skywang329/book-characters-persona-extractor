def hyponyms(li):
	return [x.hyponyms() for x in li]

def hypernyms(li):
	return [x.hypernyms() for x in li]

def flatten(li):
    newl = []
    for el in li:
        if isinstance(el, list) and not isinstance(el, basestring):
            for sub in flatten(el):
                newl.append(sub)
        else:
            newl.append(el)
    return newl

def hyponyms_list(li):
	if li:
		return flatten(hyponyms(li))
	
def hypernyms_list(li):
	if li:
		return flatten(hypernyms(li))

def get_the_hyponyms(li, hyps):
	if li:
		li += hyps
		get_the_hyponyms(hyponyms_list(li), hyps)
	return hyps

def get_the_hypernyms(li, hyps):
	if li:
		li += hyps
		get_the_hypernyms(hypernyms_list(li), hyps)
	return hyps

def get_all_hyponyms(li):
	hyps = []
	return get_the_hyponyms(li, hyps)

def get_all_hypernyms(li):
	hyps = []
	return get_the_hypernyms(li, hyps)

def synsets(wn, string, *args):
	if args:
		return wn.synsets(string, pos = args[0])
	else:
		return wn.synsets(string)

def lemmas(wn, string):
	return wn.lemmas(string)

def lemmas_list(li):
	return flatten([sense.lemmas() for sense in li])

def synsets_list(li):
	return list(set(flatten([sense.synset() for sense in li])))

def derivationally_related_forms(li):
	return flatten([sense.derivationally_related_forms() for sense in li])

def derived_forms(wn, string):
	return derivationally_related_forms(lemmas_list(synsets(wn, string)))
			
def noun_converted_synsets(wn, string):
	return synsets_list(derived_forms(wn, string))

def verb_or_noun(wn, string):
	return (synsets(wn, string, wn.VERB) or synsets(wn, string, wn.NOUN))

def any_in(nouns, synset_set):
	return any(synset for synset in nouns if str(synset) in synset_set)

def list_of_synsets(wn, li):
	return 	list(set(flatten([synsets(wn,string) for string in 
							 [str(a.name()).split('.')[0] for a in li]])
					)
				)

def in_sense_set(wn, synset_set, string):
	nouns = noun_converted_synsets(wn, string)	
	if nouns:
		result = any_in(nouns, synset_set)
		if not result:
			if not verb_or_noun(wn, string):
				syn_list = list_of_synsets(wn, nouns)
				return any_in(syn_list, synset_set)
			else:
				return result
		else:
			return result
	else:	
		return False
