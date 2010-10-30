import sqlite3
import alphagram

database = "db/anagrams.db"
conn = sqlite3.connect(database)

def get_anagrams(alphagram):
    cursor = conn.cursor()
    cursor.execute("select text, freq from anagrams where alphagram=? order by freq desc", (alphagram.upper(),))
    for text, freq in cursor:
        yield text, freq
