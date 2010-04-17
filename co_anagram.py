import string
import cPickle as pickle
from bag_of_letters import make_bag
from download import open_or_download

# FIXME! Once data built, put in good link
ngrams = open_or_download('coanagram_data.pickle', 'http://web.media.mit.edu/~rspeer/fake')

keylist = ngrams.keys()
keylist.sort()

def simple_anagram_numeric(bagnum):
    return ngrams.get(bagnum)

def simple_anagram(text):
    bagnum = make_bag(text)
    return simple_anagram_numeric(bagnum)

def complex_anagram_gen(bagnum):
    for key in ngrams:
        if bagnum % key == 0:
            main_list=ngrams[key]           
            main_freq=ngrams[key][0][2]
            other_list = simple_anagram_numeric(bagnum/key)
            if other_list:
                other_freq=other_list[0][2]
                main_textstr='['+('|'.join([tuple[0] for tuple in main_list]))+']'
                other_textstr='['+('|'.join([tuple[0] for tuple in other_list]))+']'
                # FIXME! Use better words representation after actually thinking
                if main_freq <= other_freq:
                    yield main_textstr+' '+other_textstr, 0, main_freq*other_freq

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
        
def multi_anagram(text, n=10):
    got = []
    bagnum = make_bag(text)
    firsttry = simple_anagram_numeric(bagnum)
    if firsttry:
        got.append((-1, firsttry[2], firsttry[0]))
    for text, words, freq in complex_anagram_gen(bagnum):
        got.append((-2, freq, text))
    got.sort()
    best = []
    used = set()
    for i in range(1, len(got)+1):
        text = got[-i][2]
        ordered = ' '.join(sorted(text.split()))
        if ordered not in used:
            used.add(ordered)
            best.append(text)
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

def anagram_dispatch(text):
    nblanks = text.count('?')
    if nblanks == 0:
        return multi_anagram(text)
    else:
        return wildcard_anagram(text)

if __name__ == '__main__': demo()

