# This originally used a library for caching results in pickles, but I'm not
# going to make you install it.

import codecs
from bag_of_letters import make_bag
import cPickle as pickle
import os.path
import string

#Want the higher frequency to win
def bagtuple_compare(tuple):
    return -tuple[2]

def ngrams_plus_wikipedia():
    print 'Loading.'
    ngrams = pickle.load(open('coanagram_data.pickle'))
    print 'Done loading.'
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
                if (bagnum not in ngrams) or (ngrams[bagnum][0][2] < 1000):
                    ngrams[bagnum] = [(text, nwords, 1000)]
                    print text
    return ngrams
    

out = open('anagram_data_big.pickle', 'wb')
pickle.dump(ngrams_plus_wikipedia(), out)
out.close()

