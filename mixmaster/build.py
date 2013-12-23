from mixmaster.wordlist import iter_wordlists
from mixmaster.lettermath import letters_to_vec, anahash, alphagram
from collections import defaultdict
import numpy as np
import json

worddata = []
count = 0
seen_alphagrams = set()
for word, freq in iter_wordlists():
    vec = letters_to_vec(word)
    alpha = alphagram(word)
    if alpha in seen_alphagrams:
        continue
    seen_alphagrams.add(alpha)
    anah = anahash(word)
    worddata.append(
        (len(word), anah, word, vec, freq)
    )
    count += 1
    if count % 10000 == 0:
        print(count, word)

worddata.sort(key=lambda entry: entry[:2])

print("Building matrix")
matrix = np.vstack(entry[3] for entry in worddata)
np.save('data/wordvecs.npy', matrix)

print("Building word frequencies")
words = np.array([entry[2] for entry in worddata])
freqs = np.array([entry[4] for entry in worddata])
np.save('data/words.npy', words)
np.save('data/freqs.npy', freqs)

offsets = defaultdict(dict)
current_group = None
current_start = None
for i, entry in enumerate(worddata):
    grouping = entry[:2]
    if grouping != current_group:
        if current_group is not None:
            offsets[current_group[0]][current_group[1]] = (current_start, i)
        current_group = grouping
        current_start = i

    if i % 10000 == 0:
        print(i, entry)

offsets[current_group[0]][current_group[1]] = (current_start, len(worddata))
with open('data/offsets.json', 'w') as outfile:
    json.dump(offsets, outfile)

