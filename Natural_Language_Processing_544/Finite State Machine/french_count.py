import sys
from fst import FST
from fsmutils import composewords

kFRENCH_TRANS = {0: "zero", 1: "un", 2: "deux", 3: "trois", 4:
                 "quatre", 5: "cinq", 6: "six", 7: "sept", 8: "huit",
                 9: "neuf", 10: "dix", 11: "onze", 12: "douze", 13:
                 "treize", 14: "quatorze", 15: "quinze", 16: "seize",
                 20: "vingt", 30: "trente", 40: "quarante", 50:
                 "cinquante", 60: "soixante", 100: "cent"}

kFRENCH_AND = 'et'

def prepare_input(integer):
    assert isinstance(integer, int) and integer < 1000 and integer >= 0, \
      "Integer out of bounds"
    if (integer >= 100): num = str(integer)
    elif (integer >= 10): num = "0" + str(integer)
    else: num = "00" + str(integer)
    return list(num)

def french_count():
    f = FST('french')

    f.add_state('hundreds')
    f.add_state('tens')
    f.add_state('units')
    f.add_state('tens-only')
    f.add_state('units-only')
    f.add_state('10s')
    f.add_state('20s-60s')
    f.add_state('70s')
    f.add_state('80s')
    f.add_state('90s')
    f.add_state('end')
    f.initial_state = 'hundreds'
    f.set_final('end')

    f.add_arc('hundreds', 'tens', [str(1)], [kFRENCH_TRANS[100]])
    f.add_arc('hundreds', 'tens-only', [str(0)], [])
    for ii in xrange(2, 10):
        f.add_arc('hundreds', 'tens', [str(ii)], [kFRENCH_TRANS[ii] + " " + kFRENCH_TRANS[100]])

    for ii in xrange(0, 10):
        if ii == 0:
            f.add_arc('tens', 'units', [str(0)], [])
            f.add_arc('tens-only', 'units-only', [str(0)], [])
        elif ii == 1:
            f.add_arc('tens', '10s', [str(ii)], [])
            f.add_arc('tens-only', '10s', [str(ii)], [])
        elif ii <= 6:
            f.add_arc('tens', '20s-60s', [str(ii)], [kFRENCH_TRANS[ii * 10]])
            f.add_arc('tens-only', '20s-60s', [str(ii)], [kFRENCH_TRANS[ii * 10]])
        elif ii == 7:
            f.add_arc('tens', '70s', [str(ii)], [kFRENCH_TRANS[60]])
            f.add_arc('tens-only', '70s', [str(ii)], [kFRENCH_TRANS[60]])
        elif ii == 8:
            f.add_arc('tens', '80s', [str(ii)], [kFRENCH_TRANS[4] + " " + kFRENCH_TRANS[20]])
            f.add_arc('tens-only', '80s', [str(ii)], [kFRENCH_TRANS[4] + " " + kFRENCH_TRANS[20]])
        else:
            f.add_arc('tens', '90s', [str(ii)], [kFRENCH_TRANS[4] + " " + kFRENCH_TRANS[20]])
            f.add_arc('tens-only', '90s', [str(ii)], [kFRENCH_TRANS[4] + " " + kFRENCH_TRANS[20]])

    for ii in xrange(0, 10):
        if ii == 0:
            f.add_arc('10s', 'end', [str(ii)], [kFRENCH_TRANS[10]])
        elif ii <= 6:
            f.add_arc('10s', 'end', [str(ii)], [kFRENCH_TRANS[ii + 10]])
        else:
            f.add_arc('10s', 'end', [str(ii)], [kFRENCH_TRANS[10] + " " + kFRENCH_TRANS[ii]])

    for ii in xrange(0, 10):
        if ii == 0:
            f.add_arc('20s-60s', 'end', [str(ii)], [])
        elif ii == 1:
            f.add_arc('20s-60s', 'end', [str(ii)], [kFRENCH_AND + " " + kFRENCH_TRANS[1]])
        else:
            f.add_arc('20s-60s', 'end', [str(ii)], [kFRENCH_TRANS[ii]])

    for ii in xrange(0, 10):
        if ii == 0:
            f.add_arc('70s', 'end', [str(ii)], [kFRENCH_TRANS[10]])
        elif ii == 1:
            f.add_arc('70s', 'end', [str(ii)], [kFRENCH_AND + " " + kFRENCH_TRANS[11]])
        elif ii <= 6:
            f.add_arc('70s', 'end', [str(ii)], [kFRENCH_TRANS[ii + 10]])
        else:
            f.add_arc('70s', 'end', [str(ii)], [kFRENCH_TRANS[10] + " " + kFRENCH_TRANS[ii]])

    for ii in xrange(0, 10):
        if ii == 0:
            f.add_arc('80s', 'end', [str(ii)], [])
        else:
            f.add_arc('80s', 'end', [str(ii)], [kFRENCH_TRANS[ii]])

    for ii in xrange(0, 10):
        if ii == 0:
            f.add_arc('90s', 'end', [str(ii)], [kFRENCH_TRANS[10]])
        elif ii <= 6:
            f.add_arc('90s', 'end', [str(ii)], [kFRENCH_TRANS[ii + 10]])
        else:
            f.add_arc('90s', 'end', [str(ii)], [kFRENCH_TRANS[10] + " " + kFRENCH_TRANS[ii]])

    for ii in xrange(0, 10):
        if ii == 0:
            f.add_arc('units', 'end', [str(ii)], [])
        else:
            f.add_arc('units', 'end', [str(ii)], [kFRENCH_TRANS[ii]])

    for ii in xrange(0, 10):
        f.add_arc('units-only', 'end', [str(ii)], [kFRENCH_TRANS[ii]])

    return f

if __name__ == '__main__':
    string_input = raw_input()
    user_input = int(string_input)
    f = french_count()
    if string_input:
        print user_input, '-->',
        print " ".join(f.transduce(prepare_input(user_input)))
