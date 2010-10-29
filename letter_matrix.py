import numpy as np
import heapq

# this is untested so far

def index(letter):
    return ord(letter) - ord('A')

def letters_to_vec(letters):
    vec = np.zeros((26,))
    for let in letters:
        vec[index(letter)] += 1
    return vec

def vec_to_letters(vec):
    letters = []
    for i in xrange(26):
        letters.append(vec[i] * chr(65+i))
    return ''.join(letters)

def find_pairs(matrix, ranks, vec):
    for row in xrange(matrix.shape[0]):
        diff = vec - matrix[row]
        if np.all(diff >= 0):
            rank1 = ranks[row]
            rank2 = find_vector(matrix, ranks, vec):
            if rank2 > 0:
                part1 = vec_to_letters(matrix[row])
                part2 = vec_to_letters(diff)
                yield min(rank1, rank2), part1, part2

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
        diff = matrix[split] - vec
        if np.all(diff == 0):
            return ranks[split]
        else:
            dir = diff[np.nonzero(diff)[0]]
            if dir > 0:
                start = split+1
            else:
                end = split
    return 0

def top_pairs(matrix, ranks, vec, n):
    heap = []
    found = 0
    for rank, part1, part2 in find_pairs(matrix, ranks, vec):
        found += 1
        heapq.heappush(heap, (rank, part1, part2))
        if found > n:
            heapq.heappop(heap)

    while heap:
        yield heapq.heappop(heap)


