import glob
from Trie import *
from Tokenizer import *
import sys
import jsonpickle

def booleanQuery(query, trie, result):
    # First: Scan query for open parenthesis and split it once we find a legal sub query
    # Second: Scan the Query for AND or OR
    # Third: Split at AND or OR, perform a query on either side based on which we split at
    # Last: Add or Intersect documents as we go

    # How do we check to make sure our phrases are encased in quotes?
    # print(query)

    # query = " ".join(query)

    # Ensure the number of open brackets = closed brackets or else return -1
    if (query.count("(") != query.count(")")):
        return -1

    # print("Query before getting subQuery", query)
    # Check to see if we have parenthesis and will need to get the subQuery
    # result will be a list

    # Q doesnt work
    #  ((war OR wanted) OR (wins)) AND winnings
    # (* OR *) AND winnings, result = [1, 2]
    # * AND winnings, result = [1u2,

    while "(" in query:
    # if "(" in query:
        q = getSubQuery(query)

        first = q[1]
        last = q[2]
        q = q[0]
        if(q == -1):
            return -1

        # print("Query before recursive call on result", q)
        # If the sub query is legal perform the boolean query on the sub query
        result.append(booleanQuery(q, trie, result))
        query = query.replace(query[first-1:last+1], "*")

    # If there are no sub queries then perform the 2 required queries, AND/OR
    # We now must parse the string for all occurrences of AND and OR
    # If OR is in the query, split at OR, then call booleanQuery on each new thingy, then combine them all together

    output = set()

    # If NOT is in the query, we must resolve that first
    # We can find all occurrences of the word, then return all the documents that do not have that word
    # If OR is in the query we will split it at OR
    # Then for each "phrase" before and after OR we will call boolean query
    # print("Query after getting subQuery", query)

    query = query.strip()
    # print(query)

    if ("OR" in query):
        query = query.split("OR")
        if ("" in query):
            return -1
        # Intersect between word and result, result being a set
        sets = []
        for phrase in query:
            # print("Phrase from OR is", phrase, query)
            sets.append(booleanQuery(phrase, trie, result))

        while (len(sets) != 0):
            output = output.union(sets.pop())
        return output

    if("AND" in query):

        query = query.split("AND")
        # Account for operator misuse
        if ("" in query):
            return -1

        # Intersect between word and result, result being a set
        sets = []
        notOperator = False
        for word in query:
            # Account for NOT in here
            if ("NOT" in word):
                word = word.split("NOT")
                word = word[1]
                notOperator = True
                if (word == ""):
                    return -1

            word = word.lower().strip()
            if (word == '*'):
                sets.append(result.pop(0))
            else:
                # Account for notOperator here
                if (notOperator):
                    notOperator = False
                    # If * then use result instead of new query
                    if(word == "*"):
                        result2 = result.pop(0)
                    else:
                        result2 = phraseQuery(word, trie)
                    docIDs = trie.getDocIDs()
                    # Now add docIDs - result2
                    sets.append(docIDs.difference(result2))
                # No inverse required
                else:
                    sets.append(phraseQuery(word, trie))

        # Intersect each set together
        output = sets.pop()
        while (len(sets) != 0):
            output = output.intersection(sets.pop())
        return output

    # Account for NOT here as well
    # If we get here this means there are no AND or OR operators
    # This means we may or may not have NOT
    # If we have  NOT, we can assume it is the first word in the file

    if ("NOT" in query):
        query = query.split("NOT")

        # Make sure not wasnt before the term
        if (query[-1] == ""):
            return -1

        query.remove("")
        if ("" in query):
            return -1

        docIDs = trie.getDocIDs()
        # Now perform query on the query[1] then subtract the result from all documents
        # Make sure to account for if the word is a *
        if query[0].strip() == "*":
            return docIDs.difference(result.pop(0))

        return docIDs.difference(phraseQuery(query[0], trie))

    if(query.strip() == "*"):
        return result.pop(0)

    # How do we differentiate between a phrase query not enclosed in quotes

    return phraseQuery(query, trie)

def getSubQuery(query):
    # Scan the query for matching open/close parenthesis, then call booleanQuery on that query
    index = 0
    first = 0
    last = 0
    open = 0
    close = 0
    found = False
    done = False
    # print(query)
    for char in query:
        if(char == "("):
            open += 1
            if(not found):
                first = index
                found = True
        if(char == ")"):
            close += 1
            if(open == close):
                last = index
                done = True
                break
        index += 1

    # Error for illegal query
    if (not done):
        # Return something bad???
        # TODO
        return -1
        pass

    subQuery = query[first+1:last]

    return subQuery, first+1, last

def phraseQuery(phrase, trie):
    # First we will tokenize the phrase using our tokenizer we used to make the index
    tokenizer = Tokenizer()
    phrase = tokenizer.stemQuery(phrase)
    result = []

    # Now get the occurrence dictionary for each word and append it to result
    for word in phrase:
        occurrences = trie.getOccurrences(word)
        # If the dict is empty do not append it
        if(occurrences != []):
            result.append(occurrences)

    # We now know that if length of result is smaller than phrase that we have no phrase matches
    # so we can return an empty list as the result
    # or no matches or something
    if(len(phrase) != len(result)):
        return []

    # Now for each key we must see if its in the next one, and if it is make sure the positions are correct
    # If we wanted to optimize this further we would make it choose the word with the smallest amount of occurrences
    # But that complicates things and goes above what is required
    result2 = set()
    requiredMatches = len(result)-1

    # Same thing, check for no occurences
    if result == []:
        return set()

    firstTerm = result[0]

    # print(result)
    for docID in firstTerm:
        # For each docID we must compare each position with position+1 in the other dictionaries
        matches = 0
        positions = firstTerm[docID]
        # print(result, positions)
        # If 0 occurrences
        if positions == 0:
            continue
        for position in positions:
            position2 = position + 1
            for i in range(1, requiredMatches+1):
                # Make sure word appears in the same document and position+1 exists
                if(docID in result[i] and position2 in result[i][docID]):
                    matches += 1
                position2 += 1

                # print(docID, position, position2, positions, matches)
        if(matches == requiredMatches):
            result2.add(docID)

    return result2

def tests():
    save = open("index.txt", "r")
    save = save.read()
    trie = jsonpickle.decode(save)

    # try:
    #     q = "stemming"
    #     q2 = booleanQuery(q, trie, [])
    #     print("Query is",q, "\tOutput is", q2)
    #     assert(q2 == {"1","2","3","4"})
    # except:
    #     print("Test fail\n")
    # else:
    #     print("Test succeed\n")
    #
    # try:
    #     q = "stemming never AND stemming increases"
    #     q2 = booleanQuery(q, trie, [])
    #     print("Query is", q, "\tOutput is", q2)
    #     assert (q2 == set()), "Test 1 fail"
    # except:
    #     print("Test fail\n")
    # else:
    #     print("Test succeed\n")
    #
    # try:
    #     q = "system AND never AND precision"
    #     q2 = booleanQuery(q, trie, [])
    #     print("Query is", q, "\tOutput is", q2)
    #     assert (q2 == {"1"}), "Test 1 fail"
    # except:
    #     print("Test fail\n")
    # else:
    #     print("Test succeed\n")
    #
    # try:
    #     # q = "(system OR vocabulary OR while) AND (at OR should)"
    #     q = "system AND (recall OR precision)"
    #     q2 = booleanQuery(q, trie, [])
    #     print("Query is", q, "\tOutput is", q2)
    #     # assert (q2 == {"4"})
    #     print("Test succeed")
    # except:
    #     print("Test fail\n")

    # q = "((war OR wanted) OR (wins)) AND winnings"
    # q = "winnings"

def legalChecker(query):
    # This function will ensure the user entered a legal query
    # Rather, will mainly check that the user correctly put quotes around phrase queries
    # And must follow AND or OR

    op = ["AND", "OR", "NOT"]
    op2 = ["AND", "OR"]
    for i in range(len(query)):
        if query[i] == "NOT" and i != 0 and query[i-1] not in op2:
            return False

        if query[i] not in op and i != len(query)-1 and query[i+1] not in op:
            return False
    return True



if __name__ == '__main__':
    # This must intelligently parse the arguments provided and query the index for all occurences
    # I think ideally we want to separate each part of the query into its own instance of Trie.getOccurences()
    # Maybe phrase queries can be a special case, or we can just check to see if they are properly in sequence afterwards, not sure


    #fake
    # save = open("index.txt", "r")
    # save = save.read()
    # trie = jsonpickle.decode(save)
    # # q = "((war OR wanted) OR (widening AND who)) AND (wins OR while)"
    # # q = "wins"
    # q = booleanQuery(q, trie, [])
    # print(q)


    directory = sys.argv[1]
    directory += "/index.txt"

    try:
        save = open(directory, "r")
        # save = open("indexTest.txt")
        save = save.read()
    except:
        print("File not found or not legal index")
        sys.exit()

    # Put the users command line arguments/ query into its own list of elements
    trie = jsonpickle.decode(save)
    query = sys.argv[2:]


    if not legalChecker(query):
        print("Invalid Query")
        sys.exit()

    query = " ".join(query)

    try:
        query = booleanQuery(query, trie, [])
        assert (query != -1)

        # make it so it returns a sorted list
        query2 = []
        for doc in query:
            query2.append(int(doc))

        query = query2
        query.sort()

    except:
        print("Invalid Query")
    else:
        if(query == set() or query == []):
            print("No results found")
        else:
            for docID in query:
                print(docID)
