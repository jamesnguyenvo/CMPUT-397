# This will be an object that returns a list of all the tokens in a document to be indexed
# nltk is not used to tokenize the document
# Instead it is done by hand, so we have more control over what is normalized

import re
# from nltk.stem.snowball import SnowballStemmer

class Tokenizer:

    def __init__(self):
        # Regex should leave punctuation that ends a sentence
        # As in, a period, question mark, or exclamation mark should count as a position
        self.regex = re.compile('[^a-zA-Z0-9.?!]')
        self.qregex = re.compile('[^a-zA-Z0-9]')
        # self.stemmer = SnowballStemmer("english")

    def stemDocument(self, document):
        # We do not need to stem but we might as well
        # We can tokenize the document non-retardedly by modifying the nltk tokenize function
        # We also need to index numbers, as well as the movie title

        # Error correct for a bad file
        try:
            file = open(document, "r", encoding='utf8')
            file2 = file.read()
            file.close()
        except:
            print("Error reading file", document)
            return []

        file = file2
        file = file.splitlines()
        # removing non alphabet characters from
        # https://stackoverflow.com/questions/275018/how-can-i-remove-chomp-a-trailing-newline-in-python
        stemmed = []

        for line in file:
            line = line.split()
            for word in line:
                word = word.lower()
                # We won't actually stem right now, just tokenize
                # stemmed.append(self.stemmer.stem(self.regex.sub('',word)))
                token = self.qregex.sub('',word)
                if(token != ''):
                    stemmed.append(token)

        return stemmed

    def stemQuery(self, query):
        stemmed = []

        query = query.split()
        for word in query:
            word = word.lower()
            # We won't actually stem right now, just tokenize
            # stemmed.append(self.stemmer.stem(self.regex.sub('',word)))
            token = self.qregex.sub('', word)
            if (token != ''):
                stemmed.append(token)

        return stemmed
