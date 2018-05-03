import glob
from Trie import *
from Tokenizer import *
import sys
import jsonpickle

if __name__ == '__main__':
    # Print the index
    directory = sys.argv[1]
    directory += "/index.txt"

    try:
        save = open(directory, "r")
        save = save.read()
        trie = jsonpickle.decode(save)
        trie.printTrie()
    except:
        print("File not found or not legal index")

