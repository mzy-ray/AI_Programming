# import os
#
# dict = {}
# filepath = "data/lexicon"
# pathDir = os.listdir(filepath)
# print "loading lexicon data"
#
# for path in pathDir:
#     file = open("data/lexicon/" + path)
#     print "loading file " + path
#     if (path.find(".") != -1):
#         name = path[:path.find(".")]
#     else:
#         name = path
#
#     for line in file:
#         if (not line[0].isalpha()): continue
#         tokens = line.split(" ");
#         for token in tokens:
#             if (len(token) == 0):
#                 continue
#             word = token.strip(":,\n")
#             if (not dict.has_key(word)):
#                 dict[word] = []
#                 dict[word].append(name)
#             elif (name not in dict[word]):
#                 dict[word].append(name)
#             if ([-1] == ":" or token[-1] == ","):
#                 break;
#
# print "dictionary created"
import numpy as np
print -np.inf
