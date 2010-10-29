import string, math
import cPickle as pickle
from bag_of_letters import make_bag, letter_diff, unbag
from download import open_or_download

ngrams = open_or_download('anagram_data.pickle', 'http://web.media.mit.edu/~rspeer/anagram_data.pickle.gz')

keylist = ngrams.keys()
keylist.sort()

# TODO: account for ease of anagramming
unigram_freq = {
    'a': .08167,
    'b': .01492,
    'c': .02782,
    'd': .04253,
    'e': .12702,
    'f': .02228,
    'g': .02015,
    'h': .06094,
    'i': .06966,
    'j': .00153,
    'k': .00772,
    'l': .04025,
    'm': .02406,
    'n': .06749,
    'o': .07507,
    'p': .01929,
    'q': .00095,
    'r': .05987,
    's': .06327,
    't': .09056,
    'u': .02758,
    'v': .00978,
    'w': .02360,
    'x': .00150,
    'y': .01974,
    'z': .00074
}

def simple_anagram_numeric(bagnum):
    return ngrams.get(bagnum)

def simple_anagram(text):
    bagnum = make_bag(text)
    return simple_anagram_numeric(bagnum)

def leftover_score(garble):
    goodness = 1.0
    for letter in string.lowercase:
        expected = unigram_freq[letter] * len(garble)
        actual = garble.count(letter)
        if actual > expected:
            goodness *= math.pow(unigram_freq[letter], 2*(actual - expected))
    return goodness

def complex_anagram_gen(bagnum):
    for key in ngrams:
        if bagnum % key == 0:
            main_text, main_words, main_freq = ngrams[key]
            other = simple_anagram_numeric(bagnum/key)
            if other is not None:
                other_text, other_words, other_freq = other
                yield (main_text+' '+other_text, main_words+other_words,
                       min(main_freq, other_freq))
            else:
                garble = unbag(bagnum/key)
                # quick and dirty score: prefer common letters remaining
                score = float(main_freq) * leftover_score(garble)
                yield (main_text+'/'+garble, main_words+len(garble),
                       score)

def complex_anagram(text):
    bagnum = make_bag(text)
    firsttry = simple_anagram_numeric(bagnum)
    if firsttry: return firsttry[0], 1, firsttry[2]

    bestfreq = 0
    besttext = None
    for text, words, freq in complex_anagram_gen(bagnum):
        if '/' not in text and freq > bestfreq:
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
            best.append(got[-i])
            if len(used) >= n: break
    return best

def demo():
    print multi_anagram("peach winslow")

def wildcard_anagram(text, n=20):
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

