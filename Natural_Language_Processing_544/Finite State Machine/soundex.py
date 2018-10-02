from fst import FST
import string, sys
from fsmutils import composechars, trace

def letters_to_numbers():
    """
    Returns an FST that converts letters to numbers as specified by
    the soundex algorithm
    """

    # Let's define our first FST
    f1 = FST('soundex-generate')

    # Indicate that '1' is the initial state
    f1.add_state('start')
    f1.add_state('0')
    f1.add_state('1')
    f1.add_state('2')
    f1.add_state('3')
    f1.add_state('4')
    f1.add_state('5')
    f1.add_state('6')
    f1.initial_state = 'start'

    # Set all the final states
    f1.set_final('0')
    f1.set_final('1')
    f1.set_final('2')
    f1.set_final('3')
    f1.set_final('4')
    f1.set_final('5')
    f1.set_final('6')

    # Add the rest of the arcs
    for letter in string.ascii_lowercase:
        f1.add_arc('start', '0', (letter), (letter))

        if letter in ['a', 'e', 'h', 'i', 'o', 'u', 'w', 'y']:
            f1.add_arc('0', '0', (letter), ())
            f1.add_arc('1', '0', (letter), ())
            f1.add_arc('2', '0', (letter), ())
            f1.add_arc('3', '0', (letter), ())
            f1.add_arc('4', '0', (letter), ())
            f1.add_arc('5', '0', (letter), ())
            f1.add_arc('6', '0', (letter), ())
        elif letter in ['b', 'f', 'p', 'v']:
            f1.add_arc('0', '1', (letter), ('1'))
            f1.add_arc('1', '1', (letter), ())
            f1.add_arc('2', '0', (letter), ('1'))
            f1.add_arc('3', '0', (letter), ('1'))
            f1.add_arc('4', '0', (letter), ('1'))
            f1.add_arc('5', '0', (letter), ('1'))
            f1.add_arc('6', '0', (letter), ('1'))
        elif letter in ['c', 'g', 'j', 'k', 'q', 's', 'x', 'z']:
            f1.add_arc('0', '2', (letter), ('2'))
            f1.add_arc('2', '2', (letter), ())
            f1.add_arc('1', '0', (letter), ('2'))
            f1.add_arc('3', '0', (letter), ('2'))
            f1.add_arc('4', '0', (letter), ('2'))
            f1.add_arc('5', '0', (letter), ('2'))
            f1.add_arc('6', '0', (letter), ('2'))
        elif letter in ['d', 't']:
            f1.add_arc('0', '3', (letter), ('3'))
            f1.add_arc('3', '3', (letter), ())
            f1.add_arc('1', '0', (letter), ('3'))
            f1.add_arc('2', '0', (letter), ('3'))
            f1.add_arc('4', '0', (letter), ('3'))
            f1.add_arc('5', '0', (letter), ('3'))
            f1.add_arc('6', '0', (letter), ('3'))
        elif letter in ['l']:
            f1.add_arc('0', '4', (letter), ('4'))
            f1.add_arc('4', '4', (letter), ())
            f1.add_arc('1', '0', (letter), ('4'))
            f1.add_arc('2', '0', (letter), ('4'))
            f1.add_arc('3', '0', (letter), ('4'))
            f1.add_arc('5', '0', (letter), ('4'))
            f1.add_arc('6', '0', (letter), ('4'))
        elif letter in ['m', 'n']:
            f1.add_arc('0', '5', (letter), ('5'))
            f1.add_arc('5', '5', (letter), ())
            f1.add_arc('1', '0', (letter), ('5'))
            f1.add_arc('2', '0', (letter), ('5'))
            f1.add_arc('3', '0', (letter), ('5'))
            f1.add_arc('4', '0', (letter), ('5'))
            f1.add_arc('6', '0', (letter), ('5'))
        elif letter in ['r']:
            f1.add_arc('0', '6', (letter), ('6'))
            f1.add_arc('6', '6', (letter), ())
            f1.add_arc('1', '0', (letter), ('6'))
            f1.add_arc('2', '0', (letter), ('6'))
            f1.add_arc('3', '0', (letter), ('6'))
            f1.add_arc('4', '0', (letter), ('6'))
            f1.add_arc('5', '0', (letter), ('6'))

    for letter in string.ascii_uppercase:
        f1.add_arc('start', '0', (letter), (letter))

    return f1

    # The stub code above converts all letters except the first into '0'.
    # How can you change it to do the right conversion?

def truncate_to_three_digits():
    """
    Create an FST that will truncate a soundex string to three digits
    """

    # Ok so now let's do the second FST, the one that will truncate
    # the number of digits to 3
    f2 = FST('soundex-truncate')

    # Indicate initial and final states
    f2.add_state('0')
    f2.add_state('1')
    f2.add_state('2')
    f2.add_state('3')
    f2.add_state('4')
    f2.initial_state = '0'
    f2.set_final('1')
    f2.set_final('2')
    f2.set_final('3')
    f2.set_final('4')

    # Add the arcs
    for letter in string.letters:
        f2.add_arc('0', '1', (letter), (letter))

    for n in range(10):
        f2.add_arc('0', '2', (str(n)), (str(n)))
        f2.add_arc('1', '2', (str(n)), (str(n)))
        f2.add_arc('2', '3', (str(n)), (str(n)))
        f2.add_arc('3', '4', (str(n)), (str(n)))
        f2.add_arc('4', '4', (str(n)), ())

    return f2

    # The above stub code doesn't do any truncating at all -- it passes letter and number input through
    # what changes would make it truncate digits to 3?

def add_zero_padding():
    # Now, the third fst - the zero-padding fst
    f3 = FST('soundex-padzero')

    f3.add_state('0')
    f3.add_state('1')
    f3.add_state('2')
    f3.add_state('3')
    f3.add_state('4')
    # f3.add_state('2e')
    # f3.add_state('3e')
    # f3.add_state('4e')
    
    f3.initial_state = '0'
    f3.set_final('4')
    # f3.set_final('4e')

    f3.add_arc('1', '2', (), ('0'))
    f3.add_arc('2', '3', (), ('0'))
    f3.add_arc('3', '4', (), ('0'))
    for letter in string.letters:
        f3.add_arc('0', '1', (letter), (letter))
    for number in xrange(10):
        f3.add_arc('0', '2', (str(number)), (str(number)))
        f3.add_arc('1', '2', (str(number)), (str(number)))
        f3.add_arc('2', '3', (str(number)), (str(number)))
        f3.add_arc('3', '4', (str(number)), (str(number)))


    # f3.add_arc('1', '2e', (), ('0'))
    # f3.add_arc('2', '3e', (), ('0'))
    # f3.add_arc('2e', '3e', (), ('0'))
    # f3.add_arc('3', '4e', (), ('0'))
    # f3.add_arc('3e', '4e', (), ('0'))

    return f3

    # The above code adds zeroes but doesn't have any padding logic. Add some!

if __name__ == '__main__':
    user_input = raw_input().strip()
    f1 = letters_to_numbers()
    f2 = truncate_to_three_digits()
    f3 = add_zero_padding()

    if user_input:
        print("%s -> %s" % (user_input, composechars(tuple(user_input), f1, f2, f3)))
        # trace(f3, user_input)
        # print("%s -> %s" % (user_input, composechars(tuple(user_input), f3)))