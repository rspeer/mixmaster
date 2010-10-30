import numpy as np
from db_lookup import get_anagrams
from alphagram import make_alpha

matrix = np.load('db/anagram_vectors.npy')
ranks = np.load('db/anagram_ranks.npy')

def simple_anagram(text):
    alpha = make_alpha(text)
    return list(get_anagrams(alpha))

def demo():
    print simple_anagram('star')

if __name__ == '__main__': demo()

