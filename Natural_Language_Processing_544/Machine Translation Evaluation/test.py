from nltk.corpus import wordnet as wn
import nltk

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


def getStems(words, postags):
    stems = []
    for i in range(0, len(words)):
        postagWn = get_wn_pos(postags[i])
        stem = wn.morphy(words[i], postagWn)
        if stem == None:
            stem = words[i]
        stems.append(stem)
    return stems

def test():
    try:
        file = open("")
        print("333")
    except:
        print("111")
        return False
    print("222")
    return True


if __name__ == "__main__":
    w1 = wn.synset('need.n.01')
    w2 = wn.synset('necessity.n.01')
    print w1.wup_similarity(w2)
    # a = 0.9
    # correct = 8.8
    # chunks = 4.0
    # p = correct / float(13)
    # r = correct / float(12)
    #
    # if correct != 0:
    #     mM = (p * r) / ((1 - a) * r + a * p)
    #     penalty = 0.5 * (chunks / correct)
    #     mM *= 1 - penalty
    # else:
    #     mM = 0
    #
    # print mM
