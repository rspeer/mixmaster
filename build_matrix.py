from letter_matrix import letters_to_vec
import numpy as np
import sqlite3
database = "db/anagrams.db"
conn = sqlite3.connect(database)
cursor = conn.cursor()

def build_matrix():
    cursor.execute("select alphagram, max(freq) from anagrams group by alphagram")
    vecs = []
    ranks = []
    for alpha, freq in cursor:
        print alpha, freq
        vecs.append(letters_to_vec(alpha))
        ranks.append(freq)
    matrix = np.vstack(vecs)
    ranks = np.array(ranks)
    
    sort_order = np.lexsort(matrix.T[::-1])
    return matrix[sort_order], ranks[sort_order]

def run():
    matrix, ranks = build_matrix()
    np.save('db/anagram_vectors.npy', matrix)
    np.save('db/anagram_ranks.npy', matrix)
    return matrix, ranks

if __name__ == '__main__':
    run()
