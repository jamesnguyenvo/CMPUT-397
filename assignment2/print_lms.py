# This prints the lms
import sqlite3 as sql

if __name__ == '__main__':

    # directory = sys.argv[1]

    conn = sql.connect("database.db")
    c = conn.cursor()

    # First we are gonna get the largest docid in the database
    # Then we are just gonna print from 0 to that number

    c.execute("SELECT max(docid) FROM data")
    maxid = c.fetchone()[0]


    for i in range(1, maxid+1):
        c.execute("SELECT word, MLE FROM data WHERE docid = ?", [i,])
        results = c.fetchall()

        # If that docid doesnt have any values skip it
        if len(results) == 0:
            continue

        # Format the line
        # We will print without the 0.5 added on for smoothing
        line = str(i) + "\t"
        for word in results:
            line += word[0] + ":" + str(word[1]-0.5) +", "
        print(line[:-2])

    conn.close()