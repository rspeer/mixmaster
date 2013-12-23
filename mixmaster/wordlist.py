"""
Utilities for reading wordlists in some kind of inconsistent formats.
"""
import re


LETTERS_RE = re.compile('^[A-Z ]+$')


def get_1gram_wordlist(filename='data/google-books-english.csv', cutoff=10000):
    # Read the Google Books 2012 1-gram wordlist, as compiled by Luminoso
    # in the `wordfreq` package.
    for line in open(filename, encoding='utf-8'):
        line = line.strip()
        word, freq = line.rsplit(',', 1)
        freq = float(freq)
        if freq < cutoff:
            break
        yield (word, freq)


def get_2gram_wordlist(filename='data/count_2w.txt'):
    # Read the Google Books 2009 2-gram wordlist, as compiled by Peter Norvig
    outlist = []
    for line in open(filename, encoding='utf-8'):
        line = line.strip()
        word, freq = line.split('\t', 1)
        freq = int(freq)
        outlist.append((word, freq))
    outlist.sort(key=lambda x: -x[1])
    return outlist


def filter_wordlist(wordfreqs):
    for word, freq in wordfreqs:
        word = word.upper()
        if LETTERS_RE.match(word):
            yield (word, freq)


def iter_wordlists():
    yield from filter_wordlist(get_1gram_wordlist())
    yield from filter_wordlist(get_2gram_wordlist())
