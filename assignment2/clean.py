# Cleans the database for testing
import sqlite3 as sql

if __name__ == '__main__':
    conn = sql.connect("database.db")
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS data;")
    conn.commit()
    c.execute("CREATE TABLE data (docid INT, word TEXT, MLE float, PRIMARY KEY (docid, word));")
    conn.commit()
    conn.close()