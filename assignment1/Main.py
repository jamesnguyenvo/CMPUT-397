# This will be the main, or where the main shit is called
# Not sure how to implement command line arguments in python yet so for now I just won't

from os import listdir
from os.path import isfile, join
import jsonpickle
import glob
from Trie import *
from Tokenizer import *
import sys

def getDocuments(path):
    # Getting all the text document movie summaries
    # https://stackoverflow.com/questions/3207219/how-do-i-list-all-files-of-a-directory?rq=1
    files = glob.glob(path)
    files2 = []

    # remove the last char of the file
    for file in files:
        # print(file[len(path)-1:])
        # files2.append(file[len(path)-1:])
        files2.append(file)
    files = files2
    return(files)

def getDocInfo(docs, path):
    # Get the docID and the document name
    docs2 = []
    for doc in docs:
        doc2 = doc
        doc = doc[len(path)-1:]
        under1 = 0
        under2 = 0
        index = 0
        first = True
        # Keep track of what underscore we have read
        # When we have read the 2nd underscore split the rest of the document
        for letter in doc:
            if (letter == "_"):
                if (first):
                    under1 = index
                    first = False
                else:
                    under2 = index
                    break
            index += 1

        # Make doc2 a list of strings for the title
        title = (doc[under2+1:-4].split("_"))
        docs2.append([doc[under1 + 1:under2], title, doc2])

    return docs2

def getTestDocInfo(docs, path):
    docs2 = []
    for doc in docs:
        doc2 = doc
        doc = doc[len(path)-1:]
        docs2.append([doc[-5],[doc[-5]], doc2])
    return docs2

def addDocsToTrie(docs, trie):
    # Takes a list of document paths and adds them to the given trie
    for doc in docs:
        tokens = tokenizer.stemDocument(doc[2])
        doc[1].reverse()
        for word in doc[1]:
            tokens.insert(0, word.lower())
        # print(tokens)
        position = 0
        for token in tokens:
            trie.addOccurence(token, doc[0], position)
            position += 1

def getArgs():
    args = []
    for arg in sys.argv:
        args.append(arg)

def query(query, trie):
    occurences = trie.getOccurrences(query)
    for docID in occurences:
        print(docID)

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
    firstTerm = result[0]

    # print(result)
    for docID in firstTerm:
        # For each docID we must compare each position with position+1 in the other dictionaries
        matches = 0
        positions = firstTerm[docID]
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

if __name__ == '__main__':
    # Variables
    trie = Trie()
    tokenizer = Tokenizer()

    path = "test/documents/*"
    docs = getDocuments(path)
    docs = getTestDocInfo(docs, path)
    addDocsToTrie(docs,trie)
    # trie.printTrie()

    q = "in"
    # q = tokenizer.stemQuery(q)
    print(q)
    # query(q,trie)
    q = phraseQuery(q, trie)
    print(q)

    pickle = jsonpickle.encode(trie)
    save = open("index.txt", "w")
    save.write(pickle)
    # Get the docID, document name, document path
    # docs = getDocInfo(docs, path)
    #print(docs)

    # Tokenize the documents and append each word and position to the Trie
    # NOTE: The index starts at the movie title, therefore the title would be position 0 and onward
    # addDocsToTrie(docs, trie)
    #
    # trie.printTrie()
    #
    # pickle = jsonpickle.encode(trie)
    # save = open("index.txt", "w")
    # save.write(pickle)
