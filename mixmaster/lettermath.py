import numpy as np
import heapq
import string
import re


LETTER_FREQS = np.array([
        0.08331452,  0.01920814,  0.04155464,  0.03997236,  0.11332581,
        0.01456622,  0.02694035,  0.02517641,  0.08116646,  0.00305369,
        0.00930784,  0.05399477,  0.02984008,  0.06982714,  0.06273243,
        0.0287359 ,  0.00204801,  0.07181286,  0.07714659,  0.06561591,
        0.03393991,  0.01232891,  0.01022719,  0.0037979 ,  0.01733258,
        0.00303336
])
LETTER_ARRAY = np.array(list(string.ascii_uppercase))


def index(letter):
    "The index of a (capital) letter in the alphabet."
    return ord(letter) - ord('A')


def standardize(letters):
    return re.sub(r'[^A-Z]', '', letters.upper())


def normalize(vec):
    "Scale a vector so it sums to 1."
    return vec / vec.sum()


def letters_to_vec(letters):
    """
    Convert a string made of capital letters into a vector of letter
    counts.
    """
    letters = standardize(letters)
    vec = np.zeros((26,))
    for let in letters:
        vec[index(let)] += 1
    return vec


def alphagram(letters):
    return ''.join(sorted(standardize(letters)))


def anahash(letters):
    """
    The 'anahash' of a word is the set of letters it contains more of than
    usual. An anagram that breaks into multiple pieces often has at least
    one of them whose anahash is a subsequence of the overall anahash.

    Anahashes are limited to 10 letters, so that there are at most 1023
    possible non-empty subsequences of them.
    """
    vec = normalize(letters_to_vec(letters))
    return anahash_vec(vec)


def anahash_vec(vec):
    while True:
        anomaly = vec - LETTER_FREQS
        letters = LETTER_ARRAY[anomaly > 0]
        if len(letters) <= 10:
            return ''.join(letters)
        else:
            vec = vec.copy() * 0.99


def gen_subsequences(letters, so_far=''):
    """
    Yield all subsequences of a string.
    """
    if len(letters) == 0:
        yield so_far
    else:
        yield from gen_subsequences(letters[1:], so_far)
        yield from gen_subsequences(letters[1:], so_far + letters[0])


def anagram_difficulty(vec):
    # Should work on a matrix also.
    vec2 = vec + LETTER_FREQS * .001
    freqs = vec2 / vec2.sum(axis=-1)[..., None]
    distance = (freqs / LETTER_FREQS) - 1
    return np.sqrt(np.sum(distance ** 2, axis=-1)) * vec.sum(axis=-1)


def combine_scores(s1, s2):
    return (s1 * s2) / (s1 + s2)


def vec_to_letters(vec):
    """
    Convert a vector of letter counts to a sorted string of capital letters.
    """
    letters = []
    for i in range(26):
        letters.append(vec[i] * chr(65+i))
    return ''.join(letters)


# Plan:
# There's a big matrix of letter vectors, sorted by (wordlength, anahash).
# There are also offsets into this matrix, stored as a dictionary of
#   wordlength -> anahash -> (start, end)
