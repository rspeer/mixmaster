Mixmaster is an anagrammer. So far it doesn't use any particularly clever
search algorithms, it just chugs through a *whole lot* of data.

And, in fact, more data makes better anagrams. It knows what words and phrases
people actually use. If you ask something else such as oneacross.com to anagram
"high ninja block move", it will tell you meaningless things like "COMBLIKE
HAVING JOHN" and "OH BELCH INVOKING JAM".

If you ask Mixmaster:

    >>> from anagram import *
    >>> simple_anagram('high ninja block move')
    ('BEING JOHN MALKOVICH', 3, 117719)

The key ideas of Mixmaster:

- Precompute everything possible.
- Consume as much data as possible.

The current data file contains precomputed anagrams of:
- All phrases of up to 3 words, used at least 10,000 times in the 2006 Google
  N-gram corpus.
- All Wikipedia article titles and redirects.
- All words in the ENABLE wordlist (as a last resort).

