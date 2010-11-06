import numpy as np
from db_lookup import get_anagrams
from alphagram import make_alpha
from letter_matrix import letters_to_vec, top_pairs, parallel
import heapq

matrix = np.load('db/anagram_vectors.npy')
ranks = np.load('db/anagram_ranks.npy')

def simple_anagram(text):
    """
    Find anagrams that can be made in one cached chunk from the given text.
    """
    alpha = make_alpha(text)
    return list(get_anagrams(alpha))

def multi_anagram(text, num=20):
    alpha = make_alpha(text)
    vec = letters_to_vec(alpha)
    heap = []
    used = set()
    found = 0
    for value, alpha1, alpha2 in top_pairs(matrix, ranks, vec, num):
        for text1, rank1 in get_anagrams(alpha1):
            for text2, rank2 in get_anagrams(alpha2):
                actual_val = parallel(rank1, rank2)
                combined_text = text1+' '+text2
                sorted_words = tuple(sorted(combined_text.split()))
                if sorted_words not in used:
                    used.add(sorted_words)
                    found += 1
                    heapq.heappush(heap, (actual_val, combined_text))
                    if found > num:
                        heapq.heappop(heap)
    heap.sort()
    heap.reverse()
    return heap

def demo():
    print multi_anagram('high ninja block move')
    print multi_anagram('the empire strikes back')

if __name__ == '__main__': demo()

