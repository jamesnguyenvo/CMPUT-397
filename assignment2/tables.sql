-- This will create the tables required for our database
-- One massive table should be enough I think
-- Or maybe multiple tables each corresponding to a document ID
-- Maybe that is better?

CREATE TABLE data (
  docid INT,
  word TEXT,
  MLE float,
  PRIMARY KEY (docid, word)
);