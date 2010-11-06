import sqlite3
import alphagram

database = "db/anagrams.db"
conn = sqlite3.connect(database)

def get_anagrams(alphagram):
    cursor = conn.cursor()
    cursor.execute("select text, freq from anagrams where alphagram=? order by freq desc", (alphagram.upper(),))
    used = set()
    for text, freq in cursor:
        if text not in used:
            used.add(text)
            yield text, freq
