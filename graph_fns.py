import itertools
import pickle

sentence_token = {}
sentence = {}
character_occurences = {}


with open('variable.pkl', 'rb') as fp:
	variable = pickle.load(fp)
	
for key in  variable.keys():
	exec(key + " = variable['" + key + "']")

def init_graph(graph, type = "set"):
	if type == "set":
		for i in range(len(character)):
			graph[i] = {}
			for j in range(len(character)):
				if j!= i:
					graph[i][j] = set({})
	elif type == "list":
		for i in range(len(character)):
			graph[i] = {}
			for j in range(len(character)):
				if j!= i:
					graph[i][j] = []
					
def fill_graph(sent_graph):
	s = 0
	people = set()
	gsent = 0
	i = 0
	while i in range(len(word)):
		string = ''
		ppl_count = 0
		sentence_token[s] = i
		
		while i < len(word) and s_id[i] == s:
			if ch_id[i] != -1 and ch_id[i] not in people:
				people.add(ch_id[i]) 
				ppl_count += 1
			
			i += 1
		
		if ppl_count > 2:
			pairs = list(itertools.permutations(people, 2))
			gsent += 1
			for x, y in pairs:
				if x != y:
					sent_graph[x][y].add(s)
		elif ppl_count == 1 and len(people) == 1:
			person = people.pop()
			if person not in character_occurences:
				character_occurences[person] = set()
			character_occurences[person].add(s)
		people.clear()
		
		s += 1
	sentence_token[s] = len(word)


def delete_redundant_keys(graph):
	del_key = []
	for key in graph:
		for val in graph[key]:
			if len(graph[key][val]) == 0:
				del_key.append((key,val))
		
	for i, j in del_key:
		del graph[i][j]
		
	del del_key[:]
	for key in graph:
		if len(graph[key]) == 0:
			del_key.append(key)
			
	for i in del_key:
		#not_chars.append(character[i])
		del graph[i]


def print_graph():
	count = 0
	big_count = 0
	for key in graph:
		print '\n-----------------------------------------\n'
		print '\n\n', character[key], '--- ', key, '\n\n'
		#for j in nested_keys:
		for val in graph[key]:
			#if len(graph[key][val]) == 0:
			#	count += 1
			#else:
			if 1:
				print '\n-----------------\n'
				print character[val], '- ', key, ' ', val, '\n\n'
				print graph[key][val]
			big_count += 1
		print '\n-----------------------------------------\n'

def return_sentence():
	return sentence
	
def return_sentence_token():
	return sentence_token

def return_character_occurences():
	return character_occurences
	

sents = max(set(s_id))
