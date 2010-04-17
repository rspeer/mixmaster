# This originally used a library for caching results in pickles, but I'm not
# going to make you install it.

import codecs
from bag_of_letters import make_bag
import cPickle as pickle
import os.path

max_coanagrams=10

#Want the higher frequency to win
def bagtuple_compare(tuple):
    return -tuple[2]

def ngram_data():
    ngrams = {}
    for filename in ['1grams.txt']:
#    for filename in ['1grams.txt', '2grams.txt', '3grams.txt']:
        for line in codecs.open('../../ngrams/'+filename, encoding='utf-8'):
            if line.strip():
                words, freq = eval(line)
                nwords = len(words)
                if freq >= 10000:
                    text = ' '.join(words)
                    bagnum = make_bag(text)
                    bagtuple=(text, nwords, freq)
                    if bagnum not in ngrams:
                        ngrams[bagnum] = [bagtuple]
                    elif (freq > ngrams[bagnum][-1][2]):
                        # we found a better anagram, let's see if it stays in the top n
                        ngrams[bagnum].append(bagtuple)
                        ngrams[bagnum].sort(key=bagtuple_compare)
                        ngrams[bagnum]=ngrams[bagnum][:10]
                        if bagtuple in ngrams[bagnum]:
                            print bagtuple
    return ngrams

def ngrams_plus_dictionary():
    ngrams = ngram_data()
    for line in open('enable1.txt'):
        if line.strip():
            text = line.strip().upper()
            bagnum = make_bag(text)
            if bagnum not in ngrams:
                ngrams[bagnum] = (text, 1, 100)
                print text
    return ngrams

def ngrams_plus_wikipedia():
    ngrams = ngrams_plus_dictionary()
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
                bagnum = make_bag(text)
                if (bagnum not in ngrams) or (ngrams[bagnum][2] < 1000):
                    ngrams[bagnum] = (text, nwords, 1000)
                    print text
    return ngrams
    
out = open('coanagram_data.pickle', 'wb')
pickle.dump(ngrams_plus_dictionary(), out)
out.close()

