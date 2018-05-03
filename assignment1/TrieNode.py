# This is going to be our linked list implementation for the trie
# should it be a doubly linked list?
# na, because we dont need to go backwards, we can just store each character somewhere easily

class TrieNode:

    def __init__(self, value):
        self.value = value
        self.children = dict()

    def addChild(self, node):
        self.children[node.getValue()] = node

    def getValue(self):
        return self.value

    def getChildren(self):
        return self.children

    def printChildren(self,word):
        word2 = word[:]
        word2.append(self.value)
        if (len(self.children) == 0):
            return
        for child in self.children:
            if(child == "+"):
                # Print according to assignment specs here
                word3 = "".join(word2)
                docpos = []
                index = self.children["+"]

                # For docID in index
                for pos in index:
                    docpos.append(str(pos) + ":")
                    for val in index[pos]:
                        docpos.append(str(val))
                        docpos.append(",")

                    docpos[-1] = ";"
                docpos[-1] = ""
                docpos = "".join(docpos)
                print(word3+"\t", docpos)
            else:
                self.children[child].printChildren(word2)

    def printChildrenNOWORD(self):
        if (len(self.children) == 0):
            return
        for child in self.children:
            if(child == "+"):
                print(self.children["+"])
            else:
                self.children[child].printChildren()


    def __str__(self):
        return self.value