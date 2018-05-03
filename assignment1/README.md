# Assignment 1 README:

Compilation instructions
1. in cmd run pip3 install -U jsonpickle


Assumptions:
1. in boolean_query: if you want to query an operator it must be lowercase
1. in boolean_query: all operators must be UPPERCASE
1. in boolean_query: AND is treated as cat OR dog (pig AND bird) OR doggo
// in other words its treated like multiplication in mathematical order or operations
1. in vs_query: will not print documents with a score of 0, so if the k is too high it will just end
1. in vs_query: will be at least more than 100 documents, otherwise the log and floats will be too small to exist

Collaborations:
1. https://stackoverflow.com/questions/275018/how-can-i-remove-chomp-a-trailing-newline-in-python
2. https://stackoverflow.com/questions/3207219/how-do-i-list-all-files-of-a-directory?rq=1
3. Python documentation, jsonpickle documentation

Test/Test Cases (just run them in terminal with no arguments):
1. boolean_test.py
    * Requires index.txt (built from cmput_2k_movies directory)
1. vs_test.txt 
    * Requires index.py (built from cmput_2k_movies directory)
1. print_test.py 
    * Requires indexTest.txt (built from test/test directory)

