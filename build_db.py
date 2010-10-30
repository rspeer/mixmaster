import codecs
from alphagram import make_alpha
import cPickle as pickle
import os.path
import sqlite3
import string

min_freq = 10000
#max_ngrams = 3

# YOU will need to create a database with this name using the sqlite3 tool,
# containing a table named 'anagrams' with four columns that will accept
# (string, string, int, int). This script will populate it.
database = "db/anagrams.db"

def setup_database(c):
    c.execute("create table anagrams (alphagram string, text string, nwords int, freq int)")
    for column in ('alphagram', 'text', 'freq'):
        c.execute("create index anagrams_%s on anagrams (%s)" % (column, column))

def emit(c, alpha, text, nwords, freq):
    c.execute("insert into anagrams values (?, ?, ?, ?)", (alpha, text, nwords, freq))
    print alpha, text, nwords, freq

def generate_ngram_data(c):
    for filename in ['1grams.txt', '2grams.txt', '3grams.txt']:
        for line in codecs.open('ngrams/'+filename, encoding='utf-8'):
            if line.strip():
                words, freq = eval(line)
                nwords = len(words)
                if freq >= min_freq:
                    text = ' '.join(words)
                    alpha = make_alpha(text)
                    emit(c, alpha, text, nwords, freq)

def generate_dictionary(c):
    for line in open('enable1.txt'):
        if line.strip():
            text = line.strip().upper()
            alpha = make_alpha(text)
            emit(c, alpha, text, 1, 100)

def generate_wikipedia(c):
    for line in codecs.open('enwiki-titles', encoding='utf-8'):
        line = line.strip().upper()
        if line:
            if any([ord(ch) > 127 for ch in line]): continue
            chars = []
            space = True
            parens = 0
            for ch in line:
                if parens:
                    if ch == '(': parens += 1
                    if ch == ')': parens -= 1
                else:
                    if ch in string.uppercase:
                        chars.append(ch)
                        space = False
                    elif ch == '(':
                        parens += 1
                    elif space == False:
                        chars.append(' ')
                        space = True
            if chars:
                text = ''.join(chars)
                nwords = len(text.split())
                alpha = make_alpha(text)
                emit(c, alpha, text, nwords, 10000*nwords)

conn = sqlite3.connect(database)
c = conn.cursor()
#setup_database(c)
#generate_ngram_data(c)
#generate_dictionary(c)
generate_wikipedia(c)
conn.commit()
c.close()

