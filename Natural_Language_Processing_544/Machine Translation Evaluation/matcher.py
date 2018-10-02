import nltk
from nltk.corpus import wordnet as wn


def get_wn_pos(postag):
    if postag[1].startswith('N'):
        return wn.NOUN
    elif postag[1].startswith('V'):
        return wn.VERB
    elif postag[1].startswith('J'):
        return wn.ADJ
    elif postag[1].startswith('R'):
        return wn.ADV
    else:
        return None


def getStemsP(words, postags):
    stems = []
    for i in range(0, len(words)):
        postagWn = get_wn_pos(postags[i])
        stem = None
        try:
            stem = wn.morphy(words[i], postagWn)
        except:
            pass
        if stem == None:
            stem = words[i]
        else:
            stem = stem.encode('utf-8')
        stems.append(stem)
    return stems


def getStems(words):
    stems = []
    for i in range(0, len(words)):
        stem = None
        try:
            stem = wn.morphy(words[i])
        except:
            pass
        if stem == None:
            stem = words[i]
        else:
            stem = stem.encode('utf-8')
        stems.append(stem)
    return stems


def match(h, ref):
    correct = 0.0
    chunks = 0.0
    # postagRef = nltk.pos_tag(ref)
    # postagH = nltk.pos_tag(h)
    # stemsRef = getStemsP(ref, postagRef)
    # stemsH = getStemsP(h, postagH)
    stemsRef = getStems(ref)
    stemsH = getStems(h)
    matchedRef = [-1] * len(ref)
    matchedH = [-1] * len(h)

    #exact match
    for i in range(0, len(ref)):
        for j in range(0, len(h)):
            if ref[i] == h[j] and matchedH[j] == -1:
                matchedRef[i] = j
                matchedH[j] = i
                correct += 1.0
                break

    #stem match
    for i in range(0, len(ref)):
        if matchedRef[i] != -1:
            continue
        for j in range(0, len(h)):
            if matchedH[j] == -1 and stemsRef[i] == stemsH[j]:
                matchedRef[i] = j
                matchedH[j] = i
                correct += 0.8
                break

    #synonym match
    for i in range(0, len(ref)):
        if matchedRef[i] != -1:
            continue
        for j in range(0, len(h)):
            if matchedH[j] == -1 and isSynonym(ref[i], h[j]):
                matchedRef[i] = j
                matchedH[j] = i
                correct += 0.6
                break

    #calculate the number of correct matches
    # for i in range(0, len(ref)):
    #     if matchedRef[i] != -1:
    #         correct += 1.0

    #calculate the number of chunks
    i = 0
    while i < len(ref):
        if matchedRef[i] == -1:
            chunks += 1.0
        # if matchedRef[i] != -1:
        #     chunks += 1.0
        #
        #     j = i + 1
        #     while j < len(ref) and matchedRef[j] != -1:
        #         j += 1
        #
        #     if j == i + 1:
        #         i = j
        #         continue
        #
        #     chunk = []
        #     for k in range(i, j):
        #         chunk.append(matchedRef[k])
        #     chunk.sort()
        #     prev = chunk[0]
        #     for l in range(1, len(chunk)):
        #         if chunk[l] != prev + 1:
        #             chunks += 1.0
        #         prev = chunk[l]
        #
        #     i = j
        # else:
        #     i += 1
    # print ref
    # print h
    # print correct, chunks

    return [correct, chunks]


def isSynonym(wRef, wH):
    synsets1 = []
    try:
        synsets1 = wn.synsets(wRef)
    except:
        return False
    if len(synsets1) == 0:
        return False

    synsets2 = []
    try:
        synsets2 = wn.synsets(wH)
    except:
        return False
    if len(synsets2) == 0:
        return False

    for s1 in synsets1:
        for s2 in synsets2:
            if s1 == s2:
            # if s1 == s2 or s1.wup_similarity(s2) > 0.9:
                # print wRef + " : " + wH
                return True

    return False

