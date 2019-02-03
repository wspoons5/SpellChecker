def main():
	string = "able"
	candidateSet = candidates(string)
	print(candidateSet)

def candidates(string):
	masterSet = set()
	replacements(string, masterSet)
	deletions(string, masterSet)
	swaps(string, masterSet)
	inserts(string, masterSet)
	for item in masterSet.copy():
		replacements(item, masterSet)
		deletions(item, masterSet)
		swaps(item, masterSet)
		inserts(item, masterSet)

	return masterSet
	
def replacements(string, masterSet):
	n = len(string)
	replaceSet = set()
	for i in range(n):
		for j in range(97,123):
			new = string[:i] + chr(j) + string[i + 1:]
			masterSet.add(new)

def deletions(string, masterSet):
	n = len(string)
	deleteSet = set()
	for i in range(n):
		new = string[:i] + string[i+1:]
		masterSet.add(new)

def swaps(string, masterSet):
	n = len(string)
	swapSet = set()
	for i in range(n - 1):
		new = string[:i] + string[i + 1] + string[i] + string[i + 2:]
		masterSet.add(new)

def inserts(string, masterSet):
	n = len(string)
	insertSet = set()
	for i in range(n + 1):
		for j in range(97,123):
			if i == 0:
				new = chr(j) + string
			elif i == n:
				new = string + chr(j)
			else:
				new = string[:i] + chr(j) + string[i:]
			masterSet.add(new)

main()