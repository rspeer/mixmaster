import re


LETTERS_RE = re.compile('^[A-Z]+$')

def get_wordlist(filename='mixmaster/data/google-books-english.csv', cutoff=70000):
    for line in open(filename, encoding='utf-8'):
        line = line.strip()
        word, freq = line.rsplit(',', 1)
        freq = float(freq)
        if freq < cutoff:
            break
        yield (word, freq)

def get_wordlist_filtered(filename='mixmaster/data/google-books-english.csv', cutoff=70000):
    for word, freq in get_wordlist(filename, cutoff):
        word = word.upper()
        if LETTERS_RE.match(word):
            yield (word, freq)

