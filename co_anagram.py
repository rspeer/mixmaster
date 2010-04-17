import string
import cPickle as pickle
from bag_of_letters import make_bag
from download import open_or_download

# FIXME! Once data built, put in good link
ngrams = open_or_download('coanagram_data.pickle', 'http://web.media.mit.edu/~rspeer/fake')

keylist = ngrams.keys()
keylist.sort()

default_cutoff_factor=0.2

def simple_anagram_numeric(bagnum):
    return ngrams.get(bagnum, [])

def simple_anagram(text):
    bagnum = make_bag(text)
    return simple_anagram_numeric(bagnum)

def complex_anagram_gen(bagnum, cutoff_factor=default_cutoff_factor):
    for key in ngrams:
        if bagnum % key == 0:
            main_list=ngrams[key]
            for main_text, main_words, main_freq in main_list:
                other_list = simple_anagram_numeric(bagnum/key)
                for other_text, other_words, other_freq in other_list:
                    yield (main_text+' '+other_text, main_words+other_words,
                           min(main_freq, other_freq))

def complex_anagram(text):
    bagnum = make_bag(text)
    firsttry = simple_anagram_numeric(bagnum)
    if firsttry: return firsttry[0], 1, firsttry[2]

    bestfreq = 0
    besttext = None
    for text, words, freq in complex_anagram_gen(bagnum):
        if freq > bestfreq:
            besttext, bestfreq = text, freq
    return besttext, 2, bestfreq
        
def multi_anagram(text, n=10, cutoff_factor=default_cutoff_factor):
    got = []
    bagnum = make_bag(text)
    firsttry = simple_anagram_numeric(bagnum)
    for text, words, freq in firsttry:
        got.append((-1, freq, text))
    for text, words, freq in complex_anagram_gen(bagnum, cutoff_factor):
        got.append((-2, freq, text))
    got.sort()
    best = []
    used = set()
    for i in range(1, len(got)+1):
        text = got[-i][2]
        ordered = ' '.join(sorted(text.split()))
        if ordered not in used:
            used.add(ordered)
            best.append(got[-i])
            if len(used) >= n: break
    return best
    
def demo():
    print simple_anagram("ogle gobot")
    print multi_anagram("peach winslow")

def wildcard_anagram(text, n=10):
    nblanks = text.count('?')
    if nblanks > 4:
        return ['That has too many blanks.']
    strings = [text]
    for i in range(nblanks):
        new_strings = [st + c for st in strings for c in string.lowercase]
        strings = new_strings
    got = []
    for anastring in strings:
        simple = simple_anagram(anastring)
        if simple:
            newtext, words, freq = simple
            got.append((freq, newtext))
    got.sort()
    best = []
    used = set()
    for i in range(1, len(got)+1):
        text = got[-i][1]
        ordered = ' '.join(sorted(text.split()))
        if ordered not in used:
            used.add(ordered)
            best.append(text)
            if len(used) >= n: break
    return best

def anagram_dispatch(text, n=10, cutoff_factor=default_cutoff_factor):
    nblanks = text.count('?')
    if nblanks == 0:
        return multi_anagram(text, n, cutoff_factor)
    else:
        return wildcard_anagram(text, n, cutoff_factor)

if __name__ == '__main__': demo()

