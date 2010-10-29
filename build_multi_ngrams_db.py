import codecs
from alphagram import make_alpha
import cPickle as pickle
import os.path

min_freq = 10000
#max_ngrams = 3

# YOU will need to create a database with this name using the sqlite3 tool,
# containing a table named 'anagrams' with four columns that will accept
# (string, string, int, int). This script will populate it.
database = "./ngramdb"

def emit(c, alpha, text, nwords, freq):
    c.execute("insert into anagrams values (?, ?, ?, ?)", (alpha, text, nwords, freq))
    print("insert into anagrams values (?, ?, ?, ?)", (alpha, text, nwords, freq))

def generate_ngram_data(c):
    ngrams = {}
    for filename in ['3grams.txt']: #['1grams.txt', '2grams.txt', '3grams.txt']:
        for line in codecs.open('ngrams/'+filename, encoding='utf-8'):
            if line.strip():
                words, freq = eval(line)
                nwords = len(words)
                if freq >= min_freq:
                    text = ' '.join(words)
                    alpha = make_alpha(text)
                    alphatuple=(text, nwords, freq)
                    if alpha not in ngrams:
                        ngrams[alpha] = [alphatuple]
                    else:
                        ngrams[alpha].append(alphatuple)
                    emit(c, alpha, text, nwords, freq)
    return ngrams

def generate_ngrams_plus_dictionary(c):
    ngrams = generate_ngram_data(c)
    for line in open('enable1.txt'):
        if line.strip():
            text = line.strip().upper()
            alpha = make_bag(text)
            if alpha not in ngrams:
                ngrams[alpha] = [(text, 1, 100)]
                emit(c, alpha, text, 1, 100);
    return ngrams

def generate_ngrams_plus_wikipedia(c):
    ngrams = generate_ngrams_plus_dictionary(c)
    for line in codecs.open('enwiki-titles', encoding='utf-8'):
        line = line.strip().upper()
        if line:
            if any([ord(c) > 127 for c in line]): continue
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
                alpha = make_bag(text)
                if (alpha not in ngrams) or (ngrams[alpha][2] < 1000):
                    ngrams[alpha] = [(text, nwords, 1000)]
                    emit(c, alpha, text, nwords, 1000)
    return ngrams

conn = sqlite3.connect(database)
c = conn.cursor();
# We don't actually use the result, but we could
c = ""
ngrams = generate_ngrams_plus_wikipedia(c)
conn.commit();
c.close();
