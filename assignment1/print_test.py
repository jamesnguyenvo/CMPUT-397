from print_index import *
import jsonpickle

if __name__ == '__main__':
    save = open("indexTest.txt", "r")
    save = save.read()
    trie = jsonpickle.decode(save)

    # due to the nature of the function and the amount of results we must eyeball it to make sure its correct
    trie.printTrie()

    print("\nEnsure these exist")
    print("0.594;11:544...")
    print("circulated 19:210")
    print("intimidation 5:696")
    print("memories 18:55")
    print("memory 14:442, 4:210")
    print("zoos 7:504")