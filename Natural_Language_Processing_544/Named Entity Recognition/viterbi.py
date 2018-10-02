import numpy as np

def run_viterbi(emission_scores, trans_scores, start_scores, end_scores):
    """Run the Viterbi algorithm.

    N - number of tokens (length of sentence)
    L - number of labels

    As an input, you are given:
    - Emission scores, as an NxL array
    - Transition scores (Yp -> Yc), as an LxL array
    - Start transition scores (S -> Y), as an Lx1 array
    - End transition scores (Y -> E), as an Lx1 array

    You have to return a tuple (s,y), where:
    - s is the score of the best sequence
    - y is a size N array of integers representing the best sequence.
    """
    L = start_scores.shape[0]
    assert end_scores.shape[0] == L
    assert trans_scores.shape[0] == L
    assert trans_scores.shape[1] == L
    assert emission_scores.shape[1] == L
    N = emission_scores.shape[0]

    y = []
    dp_scores = []
    back_pointer = []

    for i in xrange(N):
        dp_scores.append([])
        back_pointer.append([])
        for j in xrange(L):
            if (i == 0):
                score = start_scores[j] + emission_scores[0, j]
                back = -1
            else:
                max = dp_scores[i-1][0] + trans_scores[0, j]
                back = 0
                for k in xrange(L):
                    if (dp_scores[i-1][k] + trans_scores[k, j] > max):
                        max = dp_scores[i-1][k] + trans_scores[k, j]
                        back = k
                score = max + emission_scores[i, j]
            dp_scores[i].append(score)
            back_pointer[i].append(back)

    s = dp_scores[N-1][0] + end_scores[0]
    back = 0
    for k in xrange(L):
        if (dp_scores[N-1][k] + end_scores[k] > s):
            s = dp_scores[N-1][k] + end_scores[k]
            back = k

    y.append(back)
    for i in range(N-1, 0, -1):
        y.append(back_pointer[i][back])
        back = back_pointer[i][back]
    y.reverse()

    return (s, y)
