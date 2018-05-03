import glob
from Trie import *
from Tokenizer import *
import sys
import jsonpickle 

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

def addDocsToTrie(docs, trie):
    # Takes a list of document paths and adds them to the given trie
    tokenizer = Tokenizer()
    for doc in docs:
        tokens = tokenizer.stemDocument(doc[2])
        doc[1].reverse()
        # insert thing so we can pad
        tokens.insert(0, "+")
        for word in doc[1]:
            tokens.insert(0, tokenizer.qregex.sub("", word.lower()))
        position = 0
        for token in tokens:

            if(token == "+"):
                position += 1
                continue

            # print(token)
            # If the token has !?. in it, remove it then increment position
            if(token[-1] in ".?!" and token not in "mr. ms. mrs."):
                trie.addOccurence(token[:-1], doc[0], position)
                # print(token, token[:-1])
                position += 2
                continue

            trie.addOccurence(token, doc[0], position)
            position += 1

if __name__ == '__main__':
    directory = sys.argv[1]
    directory += "/*"
    trie = Trie()
    # We should make sure the directory they enter exists
    # Create an index of all the text documents within the directory
    # Save to file named index.txt

    # Give error if index.txt already exists
    # Clever use of try/except
    # We actually want the file does not exist error
    # not sure if this is good practice or super spaghetti solution
    
    try:
        file = open("index.txt", "r")
        file.read()

    except:
        # Gets the documents in the directory
        # Then gets the docID, title, and path to each document
        # Finally adds the tokenized words from each document into the trie
        docs = getDocuments(directory)
        docs = getDocInfo(docs, directory)
        addDocsToTrie(docs, trie)

        # Save pickled trie to index.txt
        sys.setrecursionlimit(50000)
        pickle = jsonpickle.encode(trie)
        save = open("index.txt", "w")
        save.write(pickle)

    else:
        print("File already exists")



