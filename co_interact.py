from co_anagram import *

def interact_loop():
    num_results = 10
    while True:
        try:
            text = raw_input('> ')
        except EOFError:
            return

        if text.startswith('/') and ' ' in text:
            command, arg = text[1:].split(None, 1)
            if command == 'results':
                try:
                    num_results = int(arg)
                    print "Will show %d results." % num_results
                except ValueError:
                    print "Usage: /results [n]"
            continue

        best = simple_anagram(text)
        if best:
            print "Best anagram:", best[0][0]
        for goodness, freq, anagram in multi_anagram(text, num_results):
            if anagram != best:
                print anagram

if __name__ == '__main__':
    print "==Mixmaster=="
    print "Type a phrase to find interesting anagrams of it."
    interact_loop()
