def subtract(dict1, dict2):
	for key in dict2:
		if key in dict1:
			del dict1[key]
