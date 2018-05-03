import sys
import jsonpickle
from Trie import *
from Tokenizer import *
from boolean_query import booleanQuery
from math import log, sqrt
# Ranks documents according to the vector space model

'''
COSINESCORE(q)
1 ﬂoat Scores[N] = 0
2 Initialize Length[N]
3 for each query term t
4 do calculate wt,q and fetch postings list for t
5   for each pair(d,tft,d) in postings list
6   do Scores[d] += wft,d×wt,q
7 Read the array Length[d]
8 for each d
9 do Scores[d] = Scores[d]/Length[d]
10 return Top K components of Scores[]
'''

# tf =
# idf = log(n/df)

# Break it down
# To start: each query term must be given an idf score
# Each document must be given a tf-idf score

def vs_query(trie, terms):
    totalDocs = trie.getDocIDs()

    # Will be a dictionary for each terms idf
    idf = dict()
    occurrences = dict()
    totalDocs = booleanQuery(" OR ".join(terms), trie, [])
    output = []

    # Compute the idf of each query term
    # log (n / df)
    for term in terms:
        # get df for each term
        occurrences[term] = trie.getOccurrences(term)
        df = len(occurrences[term])
        if(df == 0):
            idf[term] = 0
            continue
        idf[term] = log(len(totalDocs) / df, 10)

    # For each document that contains at least one word: compute the EL, then compute EN of each word
    for doc in totalDocs:
        # doc is an ID
        el = 0
        en = dict()
        # First compute the euclidean length
        for term in terms:
            # If the word appears in the document
            if (doc in occurrences[term]):
                # count squared
                el += (len(occurrences[term][doc])) ** 2
        el = sqrt(el)

        # now compute each terms euclidean normal score
        for term in terms:
            # if the word has a count > 0
            if (doc in occurrences[term]):
                en[term] = (len(occurrences[term][doc])) / el
            else:
                en[term] = 0

        # now multiply each terms idf by each terms euclidean normal score
        # this could have been done in the previous step but nbd
        score = 0
        for term in terms:
            score += en[term] * idf[term]

        output.append([score, doc])

    output.sort()
    output.reverse()

    return output

if __name__ == '__main__':
    directory = sys.argv[1]
    directory += "/index.txt"
    k = int(sys.argv[2])
    yn = sys.argv[3]
    terms = sys.argv[4:]
    tokenizer = Tokenizer()

    try:
        save = open(directory, "r")
        # save = open("indexTest.txt", "r")
        save = save.read()
    except:
        print("File not found or not legal index")
        sys.exit()

    # Put the users command line arguments/ query into its own list of elements
    # Ensure they enter a valid query term first
    # Normalize terms

    for term in terms:
        if (" " in term):
            print("Phrase queries not supported")
            sys.exit()
    terms = tokenizer.stemQuery(" ".join(terms))

    trie = jsonpickle.decode(save)

    # Get the ordered documents
    ranked = vs_query(trie, terms)

    # Assumption if there are no documents it wont return k 0 score results
    # Print output properly
    for i in range(0,k):
        try:
            if(yn[0] == "y"):
                print(ranked[i][1], ranked[i][0])
            else:
                print(ranked[i][1])
        except:
            break




