from boolean_query import booleanQuery, legalChecker
from Tokenizer import *
import sys
import jsonpickle

# score(d,q) = g·sT(d,q) + (1−g)sB(d,q)
# for the documents
# We will give the title a weight of 0.3 and the body a weight of 0.7
# First process the query the same way we would in Boolean_query
# Then query both tries
# Then for each id in set 1:
    # if in set2, score = 1

# Maybe store scores as an inverted dictionary of floats
# with the scores as keys

if __name__ == '__main__':
    directory = sys.argv[1]
    directory += "/zone_index.txt"
    k = int(sys.argv[2])
    g = float(sys.argv[3])


    try:
        save = open(directory, "r")
        save = save.read()
    except:
        print("File not found or not legal index")
        sys.exit()

    # Put the users command line arguments/ query into its own list of elements
    tries = jsonpickle.decode(save)
    trieTitle = tries[0]
    trieBody = tries[1]

    query = sys.argv[4:]

    # run query legalizer here too
    if not legalChecker(query):
        print("Invalid Query")
        sys.exit()

    query = " ".join(query)

    try:
        queryTitle = booleanQuery(query, trieTitle, [])
        queryBody = booleanQuery(query, trieBody, [])
        assert (queryBody != -1 and queryBody != -1)
    except:
        print("Invalid Query")
    else:
        # Perform the zone scoring for the documents
        # title and body are each a set with document id's satisfying the query
        # Perform set operations to find the score of each document ID
        # We might need the 0's as well in case they request the top 2000 results
        scores = []

        # find docs with a score of 0
        noResults = queryBody.union(queryTitle)
        noResults = trieBody.getDocIDs().difference(noResults)

        # This is not correct, score must be computed based on given g
        for docID in queryTitle:
            # Check if match in body and title
            if docID in queryBody:
                # add to our scores dict
                score = (g) + ((1 - g))
                scores.append([score,docID])
            elif docID not in queryBody:
                score = (g)
                scores.append([score,docID])
        # Now subtract the title elements from the body elements so we are left with elements only in the body
        # Then append those docs to scores
        queryBody = queryBody.difference(queryTitle)
        for docID in queryBody:
            score = (1 - g)
            scores.append([score, docID])

        scores.sort()
        scores.reverse()

        # Add the score 0 files to the list
        for docID in noResults:
            scores.append([0.0, docID])

        # We now have a list of document ids and their scores sorted by high score to low score
        # Print as many as the given k
        for i in range(k):
            docID = scores[i][1]
            score = scores[i][0]
            print(docID ,"%.2f" %score)
