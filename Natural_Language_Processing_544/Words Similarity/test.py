#!/usr/bin/env python
import distsim
import re
word_to_vec_dict = distsim.load_word2vec("nyt_word2vec.4k")

file = open("word-test.v3.txt")
for line in file:
    if (line[0] == ':' or line == ""):
        groupname = ""
        echo = True
        for i in range(2, len(line)):
            groupname += line[i]
    if (line[0].isalpha()):
        words = re.split(' |\t|\n',line)
        w1 = word_to_vec_dict[words[0]]
        w2 = word_to_vec_dict[words[1]]
        w4 = word_to_vec_dict[words[3]]
        ret = distsim.show_nearest(word_to_vec_dict, w1-w2+w4, set([words[0], words[1], words[3]]), distsim.cossim_dense)
        if (echo and ret[0][0] != words[2]):
            print("group name: " + groupname + "terms: " + words[0] + " " + words[1] + " " + words[2] + " " + words[3] + "\nincorrect prediction: " + ret[0][0])
            echo = False