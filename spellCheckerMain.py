import re
import math
from collections import Counter

def main():
    getTestData()

def getTestData():
    testFile = open("testSet.txt", "r")
    outfile = open("testOutcomes.csv", "w")
    test = loadTestSet(testFile)
    outfile.write("incorrectWord,correctWord,freq,candidateCount,incorrectLength,correctLength,norvigGuess,norvigSuccess,chiSquareGuess,chiSquareSuccess,gtestGuess,gtestSuccess,bayesGuess,bayesSuccess\n")
    for word in test.keys():
        norvigGuess = norvigCorrection(word)
        norvigSuccess = 0
        chisquareGuess = chiSquareCorrection(word)
        chisquareSuccess = 0
        gtestGuess = gtestCorrection(word)
        gtestSuccess = 0
        bayesGuess = bayesCorrection(word)
        bayesSuccess = 0
        if norvigGuess == test[word]:
            norvigSuccess = 1
        if chisquareGuess == test[word]:
            chisquareSuccess = 1
        if gtestGuess == test[word]:
            gtestSuccess = 1
        if bayesGuess == test[word]:
            bayesSuccess = 1     
        freq = P(test[word])
        candidateCount = len(candidates(word))
        outfile.write("{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n".format(word, test[word], freq, candidateCount, len(word), len(test[word]),
                                                                     norvigGuess, norvigSuccess, chisquareGuess, chisquareSuccess,
                                                                     gtestGuess, gtestSuccess,bayesGuess,bayesSuccess))
    testFile.close()
    outfile.close()

def loadTestSet(testFile):
    testMap = {}
    for line in testFile:
        lineList = line.split(":")
        correct = lineList[0]
        mispellings = lineList[1].split()
        for mispelling in mispellings:
            testMap.update({mispelling : correct})
    return testMap

def bayesClassify(expected, observed):
    theSum = sum(expected)
    probs = [x/theSum for x in expected]
    return calculateProb(observed, probs)

def calculateProb(observed, expectedProbs):
    nullProb = 1
    for i in range(len(observed)):
        nullProb *= math.pow(expectedProbs[i], observed[i])/math.factorial(observed[i])
    return nullProb*math.factorial(sum(observed))

def bayesCorrection(word):
    expected = [1]*26
    for char in word:
        if 97 <= ord(char) and ord(char) <= 122:
            expected[ord(char)-97] += 1
    candidateSet = candidates(word)
    candidateMap = {}
    for candidate in candidateSet:
        observed = [1]*26
        for char in candidate:
            if 97 <= ord(char) and ord(char) <= 122:
                observed[ord(char)-97] += 1
        candidateMap.update({candidate:bayesClassify(expected,observed)})
    return max(candidateMap.keys(), key=lambda key: candidateMap[key])

def gtest(expected, observed):
    stat = 0
    for i in range(len(expected)):
        stat += observed[i]*math.log(observed[i]/expected[i])
    return 2*stat

def chisquareTest(expected, observed):
    stat = 0
    for i in range(len(expected)):
        stat += (observed[i] - expected[i])**2/expected[i]
    return stat

def gtestCorrection(word):
    expected = [1]*26
    for char in word:
        if 97 <= ord(char) and ord(char) <= 122:
            expected[ord(char)-97] += 1
    candidateSet = candidates(word)
    candidateMap = {}
    for candidate in candidateSet:
        observed = [1]*26
        for char in candidate:
            if 97 <= ord(char) and ord(char) <= 122:
                observed[ord(char)-97] += 1
        candidateMap.update({candidate:gtest(expected,observed)})
    return max(candidateMap.keys(), key=lambda key: candidateMap[key])    

def chiSquareCorrection(word):
    expected = [1]*26
    for char in word:
        if 97 <= ord(char) and ord(char) <= 122:
            expected[ord(char)-97] += 1
    candidateSet = candidates(word)
    candidateMap = {}
    for candidate in candidateSet:
        observed = [1]*26
        for char in candidate:
            if 97 <= ord(char) and ord(char) <= 122:
                observed[ord(char)-97] += 1
        candidateMap.update({candidate:chisquareTest(expected,observed)})
    return max(candidateMap.keys(), key=lambda key: candidateMap[key])

def words(text): return re.findall(r'\w+', text.lower())

WORDS = Counter(words(open('text.txt').read()))

def P(word, N=sum(WORDS.values())): 
    "Probability of `word`."
    return WORDS[word] / N

def norvigCorrection(word): 
    "Most probable spelling correction for word."
    return max(candidates(word), key=P)

def candidates(word): 
    "Generate possible spelling corrections for word."
    return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])

def known(words): 
    "The subset of `words` that appear in the dictionary of WORDS."
    return set(w for w in words if w in WORDS)

def edits1(word):
    "All edits that are one edit away from `word`."
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

def edits2(word): 
    "All edits that are two edits away from `word`."
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))

main()