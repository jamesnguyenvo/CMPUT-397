# Query the lms and return the top k documents

import sqlite3 as sql
import sys
import math
from Tokenizer import Tokenizer

if __name__ == '__main__':
    # Get the correct arguments
    # TODO ensure correct arguments are supplied
    directory = sys.argv[1]
    k = sys.argv[2]
    query = sys.argv[3:]
    terms = len(query)

    # k = 10
    # query = ["the", "cat", "sat", "on", "the", "mat"]
    # terms = len(query)

    tokenizer = Tokenizer()

    # Tokenize query
    query = " ".join(query)
    query = tokenizer.stemQuery(query)

    # Create a db file if it doesnt already exist
    # Todo Create DB file if one does not already exist

    conn = sql.connect(directory+"/database.db")
    c = conn.cursor()

    # We need to query each docid for all the words and compute the query likelihood
    # We can query sql for all the tuples that have the words
    # Then if it doesnt equal the total we can just further multiply by the log of alpha squared

    # First lets get the maxid
    c.execute("SELECT max(docid) FROM data")
    maxid = c.fetchone()[0]

    # Create the query
    # statement = "SELECT MLE FROM data WHERE docid = ? AND"
    statement = "SELECT * FROM data WHERE"
    for term in query:
        statement += " word = ? OR"

    # Chop off the trailing OR
    statement = statement[:-2]
    # statement += "GROUP BY docid"

    c.execute(statement, query)
    results = c.fetchall()

    # If none of the words exist return nothing obviously
    if len(results) == 0:
        print("No words found")
        sys.exit()

    results2 = []
    # Either way we are gonna have to go through every single result so we can just use a for loop rn
    count = 0
    score = 1.0
    oldid = results[0][0]
    for docid, word, MLE in results:

        # If the current docID does not match the previous docID we must fill with alpha(0.5)
        if docid != oldid:
            missingTerms = terms - count
            if missingTerms != 0:
                score *= math.log(0.5, 10) * missingTerms

            # This is the final score for that document, now we can add it to results2
            results2.append([10 ** score, oldid])

            # Now reset the variables
            count = 0
            score = 1.0
            oldid = docid

        score *= math.log(MLE, 10)
        count += 1

    results2.sort()
    results2.reverse()

    for i in range (0, int(k)):
        try:
            print(str(results2[i][1]).rjust(4) + "\t" + str(results2[i][0]))
        except:
            # Not that many results
            break