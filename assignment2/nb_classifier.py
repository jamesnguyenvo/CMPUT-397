# Train and test classifier

import sqlite3 as sql
import sys

if __name__ == '__main__':

    directory = sys.argv[1]
    conn = sql.connect(directory + "/database.db")
    c = conn.cursor()

    # So among other things