#!/bin/python
import os
import nltk

lexcion = {}
def preprocess_corpus(train_sents):
    """Use the sentences to do whatever preprocessing you think is suitable,
    such as counts, keeping track of rare features/words to remove, matches to lexicons,
    loading files, and so on. Avoid doing any of this in token2features, since
    that will be called on every token of every sentence.

    Of course, this is an optional function.

    Note that you can also call token2features here to aggregate feature counts, etc.
    """

    filepath = "data/lexicon"
    pathDir = os.listdir(filepath)
    print "loading lexicon data"

    for path in pathDir:
        file = open("data/lexicon/" + path)
        print "loading file " + path
        if (path.find(".") != -1):
            name = path[:path.find(".")]
        else:
            name = path

        for line in file:
            if (not line[0].isalpha()): continue
            tokens = line.split(" ");
            for token in tokens:
                if (len(token) == 0):
                    continue
                word = token.strip(":,\n")
                if (not lexcion.has_key(word)):
                    lexcion[word] = []
                    lexcion[word].append(name)
                elif (name not in lexcion[word]):
                    lexcion[word].append(name)
                if ([-1] == ":" or token[-1] == ","):
                    break;

    print "dictionary created"

    pass

def token2features(sent, i, postags, add_neighs = True):
    """Compute the features of a token.

    All the features are boolean, i.e. they appear or they do not. For the token,
    you have to return a set of strings that represent the features that *fire*
    for the token. See the code below.

    The token is at position i, and the rest of the sentence is provided as well.
    Try to make this efficient, since it is called on every token.

    One thing to note is that it is only called once per token, i.e. we do not call
    this function in the inner loops of training. So if your training is slow, it's
    not because of how long it's taking to run this code. That said, if your number
    of features is quite large, that will cause slowdowns for sure.

    add_neighs is a parameter that allows us to use this function itself in order to
    recursively add the same features, as computed for the neighbors. Of course, we do
    not want to recurse on the neighbors again, and then it is set to False (see code).
    """
    ftrs = []
    # bias
    ftrs.append("BIAS")
    # position features
    if i == 0:
        ftrs.append("SENT_BEGIN")
    if i == len(sent)-1:
        ftrs.append("SENT_END")

    # the word itself
    word = unicode(sent[i])
    ftrs.append("WORD=" + word)
    ftrs.append("LCASE=" + word.lower())
    # some features of the word
    if word.isalnum():
        ftrs.append("IS_ALNUM")
    if word.isnumeric():
        ftrs.append("IS_NUMERIC")
    if word.isdigit():
        ftrs.append("IS_DIGIT")
    if word.isupper():
        ftrs.append("IS_UPPER")
    if word.islower():
        ftrs.append("IS_LOWER")
    if word[0].isupper():
        ftrs.append("FIRST_UPPER")
        ftrs.append("FIRST_UPPER")
    if any(x.isupper() for x in word):
        ftrs.append("HAS_UPPER")
    # if "#" in word or "@" in word:
    #     ftrs.append("HAS_SYMBOL")
    # if "http" in word:
    #     ftrs.append("HAS_LINK")

    ftrs.append("LENGTH_IS_" + str(len(word)))
    ftrs.append("POSTAG_IS_" + postags[i][1])

    # use the dictionary built from the data files
    if (lexcion.has_key(word)):
        for name in lexcion[word]:
            ftrs.append("IS_"+name);

    # previous/next word feats
    if add_neighs:
        if i > 0:
            for pf in token2features(sent, i-1, postags, add_neighs = False):
                ftrs.append("PREV_" + pf)
        if i < len(sent)-1:
            for pf in token2features(sent, i+1, postags, add_neighs = False):
                ftrs.append("NEXT_" + pf)

    # return it!
    return ftrs

if __name__ == "__main__":
    sents = [
    [ "I", "love", "apple" ]
    ]
    preprocess_corpus(sents)
    for sent in sents:
        postags = nltk.pos_tag(sent)
        for i in xrange(len(sent)):
            print sent[i], ":", token2features(sent, i, postags)
