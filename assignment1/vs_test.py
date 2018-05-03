import jsonpickle
from Trie import *
from vs_query import vs_query

if __name__ == '__main__':
    save = open("index.txt", "r")
    save = save.read()
    trie = jsonpickle.decode(save)
    
    terms1 = ["love","azkaban","harry"]
    terms2 = ["heart","love","kiss"]
    terms3 = ["irate","mad","angry"]
    
    r = vs_query(trie,terms1)
    r2 = vs_query(trie,terms2)
    r3 = vs_query(trie,terms3)
    
    if(r[0][1] == '694' and r[1][1] == '689' and r[2][1] == '690'):
        print("test 1 passed")
    r = r2
    if(r[0][1] == '732' and r[1][1] == '451' and r[2][1] == '1738'):
        print("test 2 passed")
    r = r3
    if(r[0][1] == '105' and r[1][1] == '945' and r[2][1] == '750'):
        print("test 3 passed")
    
    