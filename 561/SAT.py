import copy
import random

def GenerateCNF(lines):
    num_guests = int(lines[0][0])
    num_tables = int(lines[0][1])
    cnf = []

    for i in range(1, num_guests+1):
        clause1 = []
        for j in range(1, num_tables+1):
            for k in range(j+1, num_tables+1):
                clause2 = []
                clause2.append("~X" + str(i) + "Y" + str(j))        #one person cannot be assigned to two different table
                clause2.append("~X" + str(i) + "Y" + str(k))
                cnf.append(clause2)
            clause1.append("X" + str(i)+ "Y" + str(j))   #one person must be assigned to at least one table
        cnf.append(clause1)

    for i in range(1, len(lines)):
        guest_a = lines[i][0]
        guest_b = lines[i][1]
        if lines[i][2] == "F":
            for j in range(1, num_tables+1):
                clause1 = []
                clause2 = []
                clause1.append("~X" + guest_a + "Y" + str(j))  #two friends must be assigned to the same table
                clause1.append("X" + guest_b + "Y" + str(j))
                clause2.append("~X" + guest_b + "Y" + str(j))
                clause2.append("X" + guest_a + "Y" + str(j))
                cnf.append(clause1)
                cnf.append(clause2)
        else:
            for j in range(1, num_tables + 1):
                clause = []
                clause.append("~X" + guest_a + "Y" + str(j))  #two enermies cannot be assigned to the same table
                clause.append("~X" + guest_b + "Y" + str(j))
                cnf.append(clause)
    return cnf


def DPLL(cnf, symbols):
    if len(cnf) == 0:          #return True when sentence is empty as each clause is true
        return True
    for clause in cnf:        #return Flase when some clause is empty
        if len(clause) == 0:
            return False

    p = FindPureSymbol(cnf, symbols)  #pure symbol rule
    if p != 0:
        symbols.remove(p)
        for i in range(len(cnf)-1, -1, -1):
            rm_clause = 0
            for j in range(len(cnf[i])-1, -1, -1):
                if cnf[i][j] == p or cnf[i][j] == "~" + p:
                    rm_clause = 1
                    break
            if rm_clause == 1:
                cnf.remove(cnf[i])
        return DPLL(cnf, symbols)

    p = FindUnitClause(cnf)  #unit clause rule
    if p != 0:
        if p[0] != "~":
            symbols.remove(p)
        else:
            symbols.remove(p.strip("~"))
        for i in range(len(cnf)-1, -1, -1):
            rm_clause = 0
            for j in range(len(cnf[i])-1, -1, -1):
                if cnf[i][j] == p:
                    rm_clause = 1
                    break
                elif cnf[i][j] == "~" + p or cnf[i][j] == p.strip("~"):
                    cnf[i].remove(cnf[i][j])
            if rm_clause == 1:
                cnf.remove(cnf[i])
        return DPLL(cnf, symbols)

    p = symbols[0]    #split rule
    clause1 = []
    clause2 = []
    clause1.append(p)
    clause2.append("~"+p)
    cnf2 = copy.deepcopy(cnf)
    symbols2 = copy.deepcopy(symbols)
    cnf.append(clause1)
    cnf2.append(clause2)
    return DPLL(cnf, symbols) or DPLL(cnf2, symbols2)


def FindPureSymbol(cnf, symbols):
    for symbol in symbols:
        pn_symbol = 0
        pure_symbol = 0
        for clause in cnf:
            for literal in clause:
                if literal == symbol:
                    if pn_symbol == 0:
                        pn_symbol = 1
                        pure_symbol = 1
                    elif pn_symbol == -1:
                        pure_symbol = 0
                elif literal == "~"+symbol:
                    if pn_symbol == 0:
                        pn_symbol = -1
                        pure_symbol = 1
                    elif pn_symbol == 1:
                        pure_symbol = 0
        if pure_symbol == 1:
            return symbol
    return 0


def FindUnitClause(cnf):
    for clause in cnf:
        if len(clause) == 1:
            return clause[0]
    return 0

def WalkSAT(cnf, symbols, p, max_flips):
    values_symbols = {}
    for symbol in symbols:         #initialize symbols' values randomly
        values_symbols[symbol] = random.randint(0, 1)
    for i in range(0, max_flips):
        if ModelSatisfy(cnf, values_symbols):    #return model when it satisfies the sentence
            return values_symbols
        else:
            selected_clause = SelectFalseClause(cnf, values_symbols)  #randomly pick a false clause
            if random.random() < p:      #pick a random symbol with probability p
                flip_symbol = cnf[selected_clause][random.randint(0, len(cnf[selected_clause]) - 1)].strip("~")
            else :         #pick a symbol which flips to maximize the number of true clauses
                flip_symbol = FindHuristicSymbol(cnf, selected_clause, values_symbols)
            values_symbols[flip_symbol] = 1 - values_symbols[flip_symbol]
    values_symbols = []
    return values_symbols


def ModelSatisfy(cnf, values_symbols):
    flag_cnf = True
    for clause in cnf:
        flag_clause = False
        for literal in clause:
            if literal[0] == "~" and not values_symbols[literal.strip("~")]:
                flag_clause = True
                break
            elif not literal[0] == "~" and values_symbols[literal]:
                flag_clause = True
                break
        if not flag_clause:
            flag_cnf = False
            break
    return flag_cnf


def SelectFalseClause(cnf, values_symbols):
    false_clauses = []
    for i in range(0, len(cnf)):
        flag_clause = False
        for literal in cnf[i]:
            if literal[0] == "~" and not values_symbols[literal.strip("~")]:
                flag_clause = True
                break
            elif not literal[0] == "~" and values_symbols[literal]:
                flag_clause = True
                break
        if not flag_clause:
            false_clauses.append(i)
    selected_clause = false_clauses[random.randint(0, len(false_clauses) - 1)]
    return selected_clause


def FindHuristicSymbol(cnf, selected_clause, values_symbols):
    huristic_symbol = ""
    min = len(cnf)
    for literal in cnf[selected_clause]:
        values_symbols[literal.strip("~")] = 1 - values_symbols[literal.strip("~")]

        num_false_clause = 0
        for clause in cnf:
            flag_clause = False
            for literal in clause:
                if literal[0] == "~" and not values_symbols[literal.strip("~")]:
                    flag_clause = True
                    break
                elif not literal[0] == "~" and values_symbols[literal]:
                    flag_clause = True
                    break
            if not flag_clause:
                num_false_clause += 1

        if num_false_clause <= min:
            huristic_symbol = literal.strip("~")
            min = num_false_clause

        values_symbols[literal.strip("~")] = 1 - values_symbols[literal.strip("~")]
    return huristic_symbol


if __name__ == "__main__":

    readlines = []
    input_file = open("input.txt", 'r')
    while True:
        readline = input_file.readline()
        if readline != "":
            readlines.append(readline.strip())
        if not readline:
            break
    input_file.close()

    lines = []
    for readline in readlines:
        line = readline.split(" ")
        lines.append(line)

    output_text = ""

    symbols = []
    for i in range (1, int(lines[0][0])+1):                    #generate symbols in form of XiYj, in which Xi represents person and Yj represents table
        for j in range(1, int(lines[0][1])+1):
            symbols.append("X" + str(i) + "Y" + str(j))
    cnf = GenerateCNF(lines)          #generate cnf
    symbols2 = copy.deepcopy(symbols)
    cnf2 = copy.deepcopy(cnf)

    satisfiable =  DPLL(cnf, symbols)             #use DPLL to check whether the cnf is satisfiable

    if satisfiable == True:
        output_text += "yes\n"
        values_symbols = WalkSAT(cnf2, symbols2, 0.5, 1000000)    #as we already know the cnf is satisfiable here, the max_flips is not necessary, just input a large number
        for symbol in symbols2:
            if values_symbols[symbol]:
                assignment = symbol.strip("X").split("Y")
                output_text += assignment[0] + " " + assignment[1] + "\n"
        output_text = output_text.rstrip("\n")
    else:
        output_text += "no"

    output_file = open('output.txt', 'w')
    output_file.write(output_text)
    output_file.close()