from anagram import *

def interact_loop():
    while True:
        try:
            text = raw_input('> ')
        except EOFError:
            return
        if '?' in text: best = None
        else: best = simple_anagram(text)
        if best:
            print "Best anagram:", best[2]
        for goodness, freq, anagram in multi_anagram(text):
            if anagram != best:
                print anagram

if __name__ == '__main__':
    print "==Mixmaster=="
    print "Type a phrase to find interesting anagrams of it."
    interact_loop()
