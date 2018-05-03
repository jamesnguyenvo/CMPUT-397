# This will be the trie data structure used to store our index
# A trie consists of a root that may have up to 26 children, each who may have up to 27 children and so on
# A node with a $ as the root means the name of the nodes combined is word being indexed

from TrieNode import *

class Trie:

    def __init__(self):
        # This initializes our Trie data structure
        # self.children is the list containing the nodes of the children
        self.children = dict()
        self.docIDs = set()

    def addOccurence(self, word, docID, position):
        # Add word will add a word to our trie if it doesnt exist, if it does exist it will add to the occurences
        self.docIDs.add(docID)
        children = self.children

        # Add the + character so we know when we have reached the end of the word
        word = list(word.lower())
        word.append("+")

        for letter in word:
            # If we are at the end of the word add the occurrence to the list of occurrences
            # If the occurrence list doesn't already exist
            # our occurence list will be a dictionary that contains a doc id as a key and a list of positions
            # This way we can get all doc ids through the keys, and all positions through the keyv/alues
            if(letter == "+"):
                if(letter not in children):
                    children[letter] = dict()
                    children[letter][docID] = [position]
                    return
                # If we have an occurence dict but not for that docID
                if(docID not in children[letter]):
                    children[letter][docID] = [position]
                    return

                children[letter][docID].append(position)
                return

            # If the letter is not found add it to children
            if (letter not in children):
                newNode = TrieNode(letter)
                children[letter] = newNode
                children = newNode.getChildren()
            # If the letter exists in the trie
            if(letter in children):
                children = children[letter].getChildren()

    def getOccurrences(self, word):
        word = list(word.lower())
        children = self.children
        for letter in word:
            if(letter not in children):
                return set()
            children = children[letter].getChildren()

        if("+" not in children):
            return [0]
        return children["+"]

    def printTrie(self):
        # This will print every word in the index, as well as the documentID's and positions in
        # the format specified in the assignment specifications
        # This means we will have to perform probably a DFS on the tree in order to get every value
        # wish me luck, im going in
        for child in self.children:
            self.children[child].printChildren([])

    def getDocIDs(self):
        return self.docIDs
