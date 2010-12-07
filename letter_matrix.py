import numpy as np
import heapq

unigram_freq = np.array([.08167, .01492, .02782, .04253, .12702, .02228,
.02015, .06094, .06966, .00153, .00772, .04025, .02406, .06749, .07507, .01929,
.00095, .05987, .06327, .09056, .02758, .00978, .02360, .00150, .01974, .00074
])

def parallel(x1, x2):
    return int(1.0/(1.0/x1 + 1.0/x2))

def index(letter):
    "The index of a (capital) letter in the alphabet."
    return ord(letter) - ord('A')

def letters_to_vec(letters):
    """
    Convert a string made of capital letters into a vector of letter
    counts.
    """
    vec = np.zeros((26,), dtype=np.int8)
    for let in letters:
        vec[index(let)] += 1
    return vec

def vec_to_letters(vec):
    """
    Convert a vector of letter counts to a sorted string of capital letters.
    """
    letters = []
    for i in xrange(26):
        letters.append(vec[i] * chr(65+i))
    return ''.join(letters)

def vec_anomaly(vec):
    """
    Given a vector of letters, return the difference between that letter
    distribution and the expected letter distribution for that number of
    letters.
    """
    expected = unigram_freq * np.sum(vec)
    actual = np.asarray(vec, dtype=np.float64)
    return actual - expected

def vec_goodness(vec):
    """
    Given a vector of letters, estimate its suitability for anagramming
    (as a negative number indicating log probability of forming a good
    phrase).
    """
    anomaly = vec_anomaly(vec)
    return np.sum(np.log(unigram_freq) * np.max(anomaly, 0))

def find_pairs(matrix, ranks, vec):
    """
    Given the data (a matrix of letter counts, and a vector `ranks` saying
    how good the various rows are as anagrams), find all pairs of rows that
    combine to the given `vec` of letters.
    """
    diffs = vec - matrix
    margin = np.min(diffs, axis=-1)
    good_rows = np.where(margin >= 0)[0]
    for row in good_rows:
        diff = diffs[row]
        rank1 = ranks[row]
        rank2 = find_vector(matrix, ranks, diff)
        if rank2 > 0:
            part1 = vec_to_letters(matrix[row])
            part2 = vec_to_letters(diff)
            yield parallel(rank1, rank2), part1, part2

def find_vector(matrix, ranks, vec):
    """
    Tests whether this vector exists in the sorted matrix. Returns its value
    in `ranks` if it is there, and 0 if it is not.
    """
    # binary search
    start = 0
    end = matrix.shape[0]
    while start < end:
        split = (start+end)/2
        diff = vec - matrix[split]
        if np.all(diff == 0):
            return ranks[split]
        else:
            dir = diff[np.nonzero(diff)[0][0]]
            if dir > 0:
                start = split+1
            else:
                end = split
    return 0

def top_pairs(matrix, ranks, vec, n):
    """
    Like find_pairs, but uses a heap to filter for the `n` highest-ranked
    pairs.
    """
    heap = []
    found = 0
    for rank, part1, part2 in find_pairs(matrix, ranks, vec):
        found += 1
        heapq.heappush(heap, (rank, part1, part2))
        if found > n:
            heapq.heappop(heap)
    heap.sort()
    heap.reverse()
    return heap

