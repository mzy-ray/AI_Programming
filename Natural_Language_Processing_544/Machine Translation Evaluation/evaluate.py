#!/usr/bin/env python
import argparse  # optparse is deprecated
from itertools import islice  # slicing for iterators
import matcher


def my_METEOR(h, ref):
    a = 0.9

    matches = matcher.match(h, ref)
    correct = matches[0]
    chunks = matches[1]
    p = correct / float(sum(1 for w in h))
    r = correct / float(sum(1 for w in ref))

    if correct != 0:
        mM = (p * r) / ((1 - a) * r + a * p)
        penalty = 0.5 * chunks / correct;
        mM *= penalty;
        # penalty = 0.5 * (chunks / correct)
        # mM *= 1 - penalty
    else:
        mM = 0

    return mM


def main():
    parser = argparse.ArgumentParser(description='Evaluate translation hypotheses.')
    parser.add_argument('-i', '--input', default='data/hyp1-hyp2-ref',
                        help='input file (default data/hyp1-hyp2-ref)')
    parser.add_argument('-n', '--num_sentences', default=None, type=int,
                        help='Number of hypothesis pairs to evaluate')
    # note that if x == [1, 2, 3], then x[:None] == x[:] == x (copy); no need for sys.maxint
    opts = parser.parse_args()

    # we create a generator and avoid loading all sentences into a list
    def sentences():
        with open(opts.input) as f:
            for pair in f:
                yield [sentence.strip().split() for sentence in pair.split(' ||| ')]

    # counter = 0
    # note: the -n option does not work in the original code
    for h1, h2, ref in islice(sentences(), opts.num_sentences):
        # rset = set(ref)
        h1_match = my_METEOR(h1, ref)
        h2_match = my_METEOR(h2, ref)
        # print h1_match, h2_match
        print(1 if h1_match > h2_match else  # \begin{cases}
              (0 if h1_match == h2_match
               else -1))  # \end{cases}
        # counter += 1
        # if counter % 1000 == 0:
        #     print str(counter) + " evaluated"


# convention to allow import of this file as a module
if __name__ == '__main__':
    main()