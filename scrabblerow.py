import scrabblerun as tester

resultList = set()
memoizationDict = {}

# Greedy
def author():
    return ("Nizami, Reiyyan")

def student_id():
    return "500944046"

def find_word(searchPattern, words, scoring_f, minlen, maxlen, pick, resultPattern):
    # Check if we already have an answer from this tree
    memoizationResult = memoizationDict.get(searchPattern)

    if(memoizationResult != None):
        result = memoizationResult
    else:
        result = {}

        if(len(searchPattern) == 0):
            resultList.add(resultPattern)
            return

        if(len(searchPattern) < minlen):
            resultList.add(resultPattern+searchPattern)
            return

        # Go through each word
        for word in words:
            # Loop through each character in word
            for i in range(len(word)):
                if(i < maxlen):
                    if(searchPattern[i] != '-' and searchPattern[i] != word[i]):
                        break
                    else:
                        # Result Generator
                        if((i == (len(word)-1)) and ( (i+1 <= len(searchPattern)-1 and searchPattern[i+1] == '-') or (i == len(searchPattern)-1) ) ):
                            if(len(word) >= minlen and len(word) <= maxlen):
                                updateResults(result, word, scoring_f(word))

        memoizationDict[searchPattern] = result
    
    if(len(searchPattern) > 0):
        result[searchPattern[0]] = 0

    # Create Temp vars and use them versus having them reused
    for winner in result:
        nextResultPattern = ''
        nextSearchPattern = ''
        nextMaxLen = maxlen
        
        nextResultPattern = resultPattern + winner
        nextSearchPattern = searchPattern[len(winner):]

        # I need - as a space between Chars, Result Generator above should handle any issues of a char being at this position so I might not neeed to check if [0] is '-'
        if(len(nextSearchPattern) > 1 and nextSearchPattern[0] == '-' and nextResultPattern[-1] != '-'):
            nextSearchPattern = nextSearchPattern[1:]
            nextResultPattern += '-'

        #Must modify max length, Have to adjust this when working with full 40 char length, because 30 < 40, so even if we cut 10 we ok. 
        if(nextMaxLen >= len(nextSearchPattern)):
            nextMaxLen = len(nextSearchPattern)

        if(len(nextSearchPattern) == 0):
            resultList.add(nextResultPattern)
            # return
            break
        else:
            find_word(nextSearchPattern, words, scoring_f, minlen, nextMaxLen, 1, nextResultPattern)

def fill_words(pattern, words, scoring_f, minlen, maxlen):
    resultList.clear()
    memoizationDict.clear()

    find_word(pattern, words, scoring_f, minlen, maxlen, 1, '')

    maxResult = ''
    maxScore = 0

    for item in resultList:
        itemScore = tester.score_answer(item, item, scoring_f)
        if(itemScore > maxScore):
            maxResult = item
            maxScore = itemScore

    return maxResult

# Cannot randomly delete value, if I do, it will pick the next of same length with reduced points, need to find next word with fewer chars.
def updateResults(results, word, score):
    keyToDelete = None
    dontAdd = False
    for key, value in results.items():
        if len(key) == len(word):
            if(value < score):
                keyToDelete = key
            elif(value >= score):
                dontAdd = True

    if(keyToDelete != None):
        del results[keyToDelete]
        results[word] = score
    elif(dontAdd == False):
        results[word] = score