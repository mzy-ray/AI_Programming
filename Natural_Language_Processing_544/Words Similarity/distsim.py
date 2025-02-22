from __future__ import division
import sys,json,math
import os
import numpy as np

def load_word2vec(filename):
    # Returns a dict containing a {word: numpy array for a dense word vector} mapping.
    # It loads everything into memory.
    
    w2vec={}
    with open(filename,"r") as f_in:
        for line in f_in:
            line_split=line.replace("\n","").split()
            w=line_split[0]
            vec=np.array([float(x) for x in line_split[1:]])
            w2vec[w]=vec
    return w2vec

def load_contexts(filename):
    # Returns a dict containing a {word: contextcount} mapping.
    # It loads everything into memory.

    data = {}
    for word,ccdict in stream_contexts(filename):
        data[word] = ccdict
    print "file %s has contexts for %s words" % (filename, len(data))
    return data

def stream_contexts(filename):
    # Streams through (word, countextcount) pairs.
    # Does NOT load everything at once.
    # This is a Python generator, not a normal function.
    for line in open(filename):
        word, n, ccdict = line.split("\t")
        n = int(n)
        ccdict = json.loads(ccdict)
        yield word, ccdict

def cossim_sparse(v1,v2):
    # Take two context-count dictionaries as input
    # and return the cosine similarity between the two vectors.
    # Should return a number beween 0 and 1

    dotproduct = 0
    v1length = 0
    v2length = 0
    for k in v1:
        if (k in v2):
            dotproduct += v1[k] * v2[k];
        v1length += v1[k] * v1[k];
    for k in v2:
        v2length += v2[k] * v2[k];
    cossim = dotproduct / math.sqrt(v1length * v2length)
    return cossim
    pass

def cossim_dense(v1,v2):
    # v1 and v2 are numpy arrays
    # Compute the cosine simlarity between them.
    # Should return a number between -1 and 1

    cossim = 0
    if (len(v1) == len(v2)):
        dotproduct = 0
        v1length = 0
        v2length = 0
        for i in range(0, len(v1)):
            dotproduct += v1[i] * v2[i];
            v1length += v1[i] * v1[i];
            v2length += v2[i] * v2[i];
        cossim = dotproduct / math.sqrt(v1length * v2length)
    return cossim
    pass

def show_nearest(word_2_vec, w_vec, exclude_w, sim_metric):
    #word_2_vec: a dictionary of word-context vectors. The vector could be a sparse (dictionary) or dense (numpy array).
    #w_vec: the context vector of a particular query word `w`. It could be a sparse vector (dictionary) or dense vector (numpy array).
    #exclude_w: the words you want to exclude in the responses. It is a set in python.
    #sim_metric: the similarity metric you want to use. It is a python function
    # which takes two word vectors as arguments.

    # return: an iterable (e.g. a list) of up to 10 tuples of the form (word, score) where the nth tuple indicates the nth most similar word to the input word and the similarity score of that word and the input word
    # if fewer than 10 words are available the function should return a shorter iterable
    #
    # example:
    #[(cat, 0.827517295965), (university, -0.190753135501)]

    nearest = []
    minsim = float('inf')
    for k in word_2_vec:
        if (k in exclude_w): continue
        sim = sim_metric(word_2_vec[k], w_vec)
        if (len(nearest) < 10):
            nearest.append((k, sim))
            if (sim < minsim):
                minsim = sim
        elif (sim > minsim):
            for i in range(0, len(nearest)):
                if (nearest[i][1] == minsim):
                    nearest[i] = (k, sim)
                    minsim = sim
                    break
            for w in nearest:
                if (w[1] < minsim):
                    minsim = w[1]
    nearest = sorted(nearest, key=lambda word: word[1], reverse=True)
    return nearest
    pass
