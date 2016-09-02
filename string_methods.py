def title_case(string):
	return string[0].upper() + string[1:].lower()

def stringify(li):
	return ' '.join(li)

def sentence(word_list, i):
	return stringify(word_list[i])
