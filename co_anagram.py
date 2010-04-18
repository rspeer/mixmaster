import string
import cPickle as pickle
from bag_of_letters import make_bag, unbag
from download import open_or_download

# FIXME! Once data built, put in good link
ngrams = open_or_download('coanagram_data.pickle', 'http://web.media.mit.edu/~rspeer/fake')

keylist = ngrams.keys()
keylist.sort()

def simple_anagram_numeric(bagnum):
    return ngrams.get(bagnum, [])

def simple_anagram(text):
    bagnum = make_bag(text)
    return simple_anagram_numeric(bagnum)

def complex_anagram_gen(bagnum):
    for key in ngrams:
        if bagnum % key == 0:
            main_list=ngrams[key]
            for main_text, main_words, main_freq in main_list:
                other_list = simple_anagram_numeric(bagnum/key)
                found = False
                for other_text, other_words, other_freq in other_list:
                    found = True
                    yield (main_text+' '+other_text, main_words+other_words,
                           min(main_freq, other_freq))
                if not found:
                    garble = unbag(bagnum/key)
                    words = main_words + len(garble)
                    # quick and dirty score: prefer common letters remaining
                    score = float(main_freq)/(bagnum/key)
                    yield (main_text+'/'+garble, main_words+len(garble),
                           score)

def multi_anagram(text, n=10):
    got = []
    bagnum = make_bag(text)
    firsttry = simple_anagram_numeric(bagnum)
    for text, words, freq in firsttry:
        got.append((-1, freq, text))
    for text, words, freq in complex_anagram_gen(bagnum):
        got.append((-2, freq, text))
    got.sort()
    best = []
    used = set()

    for i in range(1, n*2):
        text = got[-i][2]
        while '/' in text:
            # got a reasonable phrase plus a garble of leftover letters
            # try to do something with the rest
            print '\tRe-anagramming:', text
            before, after = text.split('/')
            reanagram = multi_anagram(after, 1)
            if reanagram:
                newtext = before+' '+reanagram[0][2]
                newfreq = min(got[-i][1], reanagram[0][1])
                got[-i] = (-3, newfreq, newtext)
                text = got[-i][2]
            else: break
    got.sort()

    for i in range(1, len(got)+1):
        text = got[-i][2]
        if '/' in text:
            # edge case where we have a garble we didn't expand
            # because it was too far down the list
            continue
        ordered = ' '.join(sorted(text.split()))
        if ordered not in used:
            used.add(ordered)
            best.append(got[-i])
            if len(used) >= n: break
    return best

def best_anagram(text):
    result = multi_anagram(text, 1)
    if result: return result[0]
    else: return None

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

def anagram_dispatch(text, n=10):
    nblanks = text.count('?')
    if nblanks == 0:
        return multi_anagram(text, n)
    else:
        return wildcard_anagram(text, n)

if __name__ == '__main__': demo()

