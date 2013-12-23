from lettermath import standardize, anagram_difficulty, anahash_vec, gen_subsequences, letters_to_vec
import numpy as np
import json

word_mat = np.load('data/wordvecs.npy')
word_array = np.load('data/words.npy')
freq_array = np.load('data/freqs.npy')


with open('data/offsets.json') as jsonfile:
    offsets = {int(length): subdict for length, subdict in json.load(jsonfile).items()}

def freq_cost(freq):
    return (40 - np.log2(freq)) * 50 + 1000


def anagram_search(letters):
    letters = standardize(letters)
    dif = anagram_difficulty(letters_to_vec(letters))

    # Queue entries contain: estimated cost, cost w/o difficulty, words so far, vec remaining
    queue = [(dif, 0, (), letters_to_vec(letters))]
    step = 0
    while queue:
        score, cost, words_so_far, vec = queue.pop()
        #if words_so_far:
        #    print(score, cost, words_so_far)
        anah = anahash_vec(vec)
        length = int(vec.sum())
        start_length = 2
        for subseq in gen_subsequences(anah):
            if subseq:
                for sublength in range(start_length, length+1):
                    start_row, end_row = offsets[sublength].get(subseq, [None, None])
                    if start_row is None:
                        continue
                    submat = word_mat[start_row:end_row]
                    diffs = vec - submat
                    valid = (np.min(diffs, -1) >= 0)
                    if np.any(valid):
                        valid_diffs = diffs[valid]
                        difficulties = anagram_difficulty(valid_diffs)
                        valid_words = word_array[start_row:end_row][valid]
                        valid_freqs = freq_array[start_row:end_row][valid]
                        for row in range(valid_diffs.shape[0]):
                            newvec = valid_diffs[row]
                            newdif = difficulties[row]
                            newword = valid_words[row]
                            newcost = freq_cost(valid_freqs[row])
                            item = (cost + newcost + newdif, cost + newcost, words_so_far + (newword,), newvec)
                            if newdif == 0:
                                yield item
                            else:
                                queue.append(item)
        queue.sort(reverse=True)
        queue = queue[-1000:]
        step += 1
        if step % 10000 == 0:
            print(step, len(queue), queue[0])
            print(newword)

