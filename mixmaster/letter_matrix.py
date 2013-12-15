import numpy as np
import heapq


LETTER_FREQS = np.array([
        0.08331452,  0.01920814,  0.04155464,  0.03997236,  0.11332581,
        0.01456622,  0.02694035,  0.02517641,  0.08116646,  0.00305369,
        0.00930784,  0.05399477,  0.02984008,  0.06982714,  0.06273243,
        0.0287359 ,  0.00204801,  0.07181286,  0.07714659,  0.06561591,
        0.03393991,  0.01232891,  0.01022719,  0.0037979 ,  0.01733258,
        0.00303336
])


def index(letter):
    "The index of a (capital) letter in the alphabet."
    return ord(letter) - ord('A')


def letters_to_vec(letters):
    """
    Convert a string made of capital letters into a vector of letter
    counts.
    """
    vec = np.zeros((26,))
    for let in letters:
        vec[index(let)] += 1
    return vec


def anagram_difficulty(vec):
    # Should work on a matrix also.
    freqs = vec / vec.sum(axis=-1)
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


def find_pairs(matrix, scores, vec):
    """
    Given the data (a matrix of letter counts, and a vector `scores` saying
    how good the various rows are as anagrams), find all pairs of rows that
    combine to the given `vec` of letters.
    """
    for row in range(matrix.shape[0]):
        diff = vec - matrix[row]
        if np.all(diff >= 0):
            score1 = scores[row]
            score2 = find_vector(matrix, scores, vec)
            if score2 > 0:
                part1 = vec_to_letters(matrix[row])
                part2 = vec_to_letters(diff)
                yield min(score1, score2), part1, part2


def find_vector(matrix, scores, vec):
    """
    Tests whether this vector exists in the sorted matrix. Returns its value
    in `scores` if it is there, and 0 if it is not.
    """
    # binary search
    start = 0
    end = matrix.shape[0]
    while start < end:
        split = (start + end) / 2
        diff = matrix[split] - vec
        if np.all(diff == 0):
            return scores[split]
        else:
            dir = diff[np.nonzero(diff)[0]]
            if dir > 0:
                start = split + 1
            else:
                end = split
    return 0


def top_pairs(matrix, scores, vec, n):
    """
    Like find_pairs, but uses a heap to filter for the `n` highest-scored
    pairs.
    """
    heap = []
    found = 0
    for score, part1, part2 in find_pairs(matrix, scores, vec):
        found += 1
        heapq.heappush(heap, (score, part1, part2))
        if found > n:
            heapq.heappop(heap)

    while heap:
        yield heapq.heappop(heap)


