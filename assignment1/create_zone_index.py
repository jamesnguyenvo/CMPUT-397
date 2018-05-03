import glob
from Trie import *
from Tokenizer import *
import sys
import jsonpickle
from create_index import getDocInfo, getDocuments

# This function will operate very similarly to the create_index of part 1
# Difference being that title and body get their own index/zone


# First lets build the zone_index.txt

def addDocsToTries(docs, trieTitle, trieBody):
    # Takes a list of document paths and adds them to the given tries
    # ID, title, body
    tokenizer = Tokenizer()
    for doc in docs:
        tokens = tokenizer.stemDocument(doc[2])
        # Add titles to title trie
        position = 0
        for word in doc[1]:
            trieTitle.addOccurence(tokenizer.qregex.sub("", word.lower()),doc[0], position)
            position += 1
        position = 0
        for token in tokens:

            # If the token has !?. in it, remove it then increment position
            if(token[-1] in ".?!" and token not in "mr. ms. mrs."):
                trieBody.addOccurence(token[:1], doc[0], position)
                position += 2
                continue

            trieBody.addOccurence(token, doc[0], position)
            position += 1

if __name__ == '__main__':
    directory = sys.argv[1]
    directory2 = sys.argv[2]
    directory += "/*"
    trieTitle = Trie()
    trieBody = Trie()

    # Give error if index.txt already exists
    # Clever use of try/except
    # We actually want the file does not exist error
    # not sure if this is good practice or super spaghetti solution

    try:
        file = open("zone_index.txt", "r")
        file.read()

    except:
        # Gets the documents in the directory
        # Then gets the docID, title, and path to each document
        # Finally adds the tokenized words from each document into the trie
        docs = getDocuments(directory)
        docs = getDocInfo(docs, directory)
        addDocsToTries(docs, trieTitle, trieBody)

        # Save pickled trie to index.txt
        sys.setrecursionlimit(50000)
        pickle = [trieTitle, trieBody]
        pickle = jsonpickle.encode(pickle)
        save = open("zone_index.txt", "w")
        save.write(pickle)

    else:
        print("File already exists")