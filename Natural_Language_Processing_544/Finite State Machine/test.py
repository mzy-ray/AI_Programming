from fst import FST
import string, sys
from fsmutils import composechars, trace

def test():
    f = FST('test')
    f.add_state('1')
    f.add_state('2')
    f.add_state('3')
    f.add_state('4')
    f.initial_state = '1'
    # f.set_final('2')
    f.set_final('4')
    f.add_arc('1', '2', ('a'), ('b'))

    f.add_arc('2', '3', ('b'), ('c'))
    f.add_arc('3', '4', ('c'), ('d'))
    f.add_arc('1', '2', (), ('s'))
    f.add_arc('2', '3', (), ('s'))
    f.add_arc('3', '4', (), ('s'))
    return f

if __name__ == '__main__':
    # user_input = raw_input().strip()
    # f = test()
    # if user_input:
    #
    #     trace(f, user_input)
    #     print("%s -> %s" % (user_input, composechars(tuple(user_input), f)))
    s = 'a'
    s2 = "b"
    print s+" "+s2