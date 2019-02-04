def main():
	wordFile = open("text.txt", "r")
	wordSet = loadWords(wordFile)
	testFile = open("testSet.txt", "r")
	test = loadTestSet(testFile)
	successes = []
	failures = {}
	for word in test.keys():
		guess = correct(word, wordSet)
		if guess == test[word]:
			successes.append(guess)
		else:
			failures.update({word: guess})

	print("{} Correct\n {} Incorrect\n {}".format(len(successes), len(failures.keys()), failures))

	wordFile.close()
	testFile.close()

def loadTestSet(testFile):
	testMap = {}
	for line in testFile:
		lineList = line.split(":")
		correct = lineList[0]
		mispellings = lineList[1].split()
		for mispelling in mispellings:
			testMap.update({mispelling : correct})
	return testMap

def correct(word, wordSet):
	if word in wordSet:
		return word
	wordCounter = letterCounter(word)
	candidateSet = candidates(word)
	possibleWords = wordSet.intersection(candidateSet)
	minVal = None
	correction = None
	for item in possibleWords:
		possibleCounter = letterCounter(item)
		chi2Stat = chiSquareTestStat(wordCounter, possibleCounter)
		if minVal == None:
			correction = item
			minVal = chi2Stat
		else:
			if chi2Stat < minVal:
				minVal = chi2Stat
				correction = item
	return correction 

def letterCounter(word):
	letterList = [1]*26
	for char in word:
		if char != "-":
			letterList[ord(char) - 97] += 1
	return letterList

def chiSquareTestStat(observed, expected):
	broken = False
	if len(observed) != len(expected):
		broken = True
		print("ERROR: The length of observed does not equal the length of expected!")

	if not broken:
		stat = 0
		for i in range(len(observed)):
			stat += (observed[i] - expected[i])**2 / expected[i]
		return stat
	return None

def loadWords(wordFile):
	wordSet = set()
	text = wordFile.read()
	wordList = text.split()
	for i in range(len(wordList)):
		uncleanedWord = wordList[i]
		word = clean(uncleanedWord.lower())
		if isWord(word):
			wordSet.add(word)
	return wordSet

def clean(word):
	removeList = ["?", ",", ".", "'", '"', "!", "*", ":", ";", "", "[", "]", "(", ")", "{", "}"]
	for char in word:
		if char in removeList:
			word = word.replace(char, "")
	return word

def isWord(word):
	for char in word:
		if not isAlpha(char) and char != "-":
			return False
	return True

def isAlpha(char):
	if 97 <= ord(char) and ord(char) <= 122:
		return True
	return False

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