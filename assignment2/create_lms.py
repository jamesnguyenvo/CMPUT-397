# Ben/ James
# This will create the lms database
# We will use an SQLite database to store our words and stuff

# Tested using the NYT and Movies
# How do we handle the 2 different data formats?
# Would this be an assumption to call the program differently?
# Should we make it treat each block of text after a linebreak as a new document with a new linebreak?


from Tokenizer import Tokenizer
import sqlite3 as sql
import sys
import glob

# This adds the documents to the SQL database
# We are going to be using basic smoothing, adding 1/2 to each MLE
def addDocuments(documents, cursor):

    alpha = 0.5
    # Read each document
    # Tokenize it, removing all punctuation and things that aren't words
    # Compute the MLE of each word, then add to DB

    tokenizer = Tokenizer()

    # Can we tell whether we were given a list or a list of lists?
    # check the type of documents[0]
    # If its a list, skip some steps, if its a string, do those steps, duh
    docid = 1
    for doc in documents:
        # Doc Id is just a counter

        # If doc != list then do these extra steps to get it into a tokenized word list
        # Tokenize the document into list of tokens
        if type(doc) is not list:
            doc = tokenizer.stemDocument(doc)

        # Im getting empty documents for some reason, this is a bandaid solution for
        # the error in getDocuments2
        if doc == []:
            continue

        # Count the occurrences of each word, and total words
        # We will do this by adding each word to a dictionary
        # There may be faster ways but this seems easy right now

        tf = {}
        totalTerms = len(doc)
        for word in doc:
            try:
                tf[word] += 1
            except:
                tf[word] = 1

        # Now for each word in the tf dictionary compute the MLA and add it to the database
        for word in tf:
            MLE = (tf[word] / totalTerms) + alpha
            values = [docid, word, MLE]
            cursor.execute("INSERT INTO data VALUES (?,?,?)", values)

        # Increment docId
        docid += 1

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
    return (files)

# This will return a list of lists, each representing a tokenized document?
# It seems there are only empty strings after the URL and after the article?
def getDocuments2(path):
    # Should find a single file now
    file = glob.glob(path)
    file = open(file[0], "r", encoding="utf8")
    file = file.read()
    file = file.splitlines()
    tokenizer = Tokenizer()

    index = 0
    output = []
    normalizedDoc = []
    for line in file:
        if line == "":
            index += 1
        line = tokenizer.stemQuery(line)
        normalizedDoc += line
        if index % 2 == 0 and index > 1: # The error is here index thing
            # Instead of returning, we want to normalize this all this and send it somewhere
            # Gonna do lots of computing though
            # Remove the URL from the normalized document

            # If we are at the end of the file normalizedDoc will be empty, so we can just stop
            if normalizedDoc == []:
                return output

            normalizedDoc.pop(0)
            normalizedDoc.pop(0)

            # Add the normlaized doc to the output list
            output.append(normalizedDoc)
            # Reset the normalizedDoc list to prepare for the next document
            normalizedDoc = []

if __name__ == '__main__':

    # Path to the documents of the corpus
    directory = sys.argv[1]
    directory += "/*"
    output = sys.argv[2]

    # directory = "new-york-times-articles/*"
    # directory = "cmput397_2k_movies/*"

    conn = sql.connect(output+"/database.db")
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS data")
    c.execute("PRAGMA foreign_keys=ON;")
    c.execute('''CREATE TABLE data (
  docid INT,
  word TEXT,
  MLE float,
  PRIMARY KEY (docid, word)
)''')
    conn.commit()

    # This code should work for the movie directory
    # Maybe if this is only 1 document we know they are all in a single file
    # In that case we can call the other one
    # It would be smarter to do it the opposite way because less grabbing I guess
    # Fix that later

    documents = getDocuments(directory)

    if len(documents) == 1:
        # Grab the single document and read it differently
        documents = getDocuments2(directory)

    addDocuments(documents,c)
    conn.commit()
    conn.close()

# Ok so we need to tokenize each document
# Then compute the MLE of each word in the document and add it to the database


