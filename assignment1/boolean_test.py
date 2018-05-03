from boolean_query import *

# test for boolean query function
if __name__ == '__main__':
    save = open("index.txt", "r")
    save = save.read()
    trie = jsonpickle.decode(save)
    
    # test for single term query
    result = booleanQuery("forgot", trie, [])
    test = set(['35', '42', '310', '604', '651','833','989','1163','1181','1290','1397','1901'])
    if result == test:
        print("Test for single term query passed.")
    else:
        print("Test for single term query failed.")

    # test for phrase query 
    result = booleanQuery('"there once"', trie, [])
    test = set(['1806'])
    if result == test:
        print("Test for phrase query passed.")
    else:
        print("Test for phrase query failed.")

    # test for term query connected with NOT operator
    result = booleanQuery('"gdr AND NOT effort"', trie, [])
    test = set(['1060'])
    if result == test:
        print("Test for term query connected with NOT operator passed.")
    else:
        print("Test for term query connected with NOT operator failed.")
